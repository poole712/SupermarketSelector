from datetime import datetime
import uuid

from langchain.agents.middleware import AgentMiddleware, ModelCallLimitMiddleware, PIIMiddleware, TodoListMiddleware
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from langchain_core.rate_limiters import InMemoryRateLimiter
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from typing import Dict, Optional, Union

from tools import get_all_tools

SYSTEM_PROMPT = f"""You are a careful supermarket price-finding assistant for New Zealand.
Use the exact store list provided by the user. Do not substitute other stores, suburbs, or chains. If the user provides a region and a store list, you must search those exact stores first.

Keep going until you have checked all requested stores and items. Do not stop early. Use non-member prices.
Accept cookies and navigate pop-ups as needed.

You explore the websites for Woolworths, PAK'nSAVE, and New World to find these essentials:
- milk
- cheese
- mince
- eggs
Use the find_store_item_name tool first to resolve a good item name for the store. Provide the tool with the store name: 'pak' for PAK'nSave, 'new' for New World, and 'wol' for Woolworths. Then use the returned item name in your search.

For each store in the provided list, search for each item individually and try multiple search variations if the first attempt fails. Build search queries in a simple, natural style such as: 'PAK'nSAVE Kilbirnie milk', 'Woolworths Kilbirnie eggs', or 'New World Newtown cheese'. Keep the query short and specific rather than over-quoting it.

Find the cheapest branded item that matches the requested size or amount. Only return null if you have tried reasonable searches and still cannot find a matching product. Never give up after the first failed search.

When filling the structured result, create one entry for each provided store using the exact store name as the key and as the store name field. Do not collapse results into generic supermarket names. If you are unsure about a price, mention that supermarket pricing can vary by location and time, and that online prices may be slightly inaccurate."""

class TolerateToolErrors(AgentMiddleware):
    """Hand tool failures back to the model as a message so it can recover, rather than
    crashing the run. Tools that touch the outside world, like a browser, fail now and then."""

    async def awrap_tool_call(self, request, handler):
        try:
            return await handler(request)
        except Exception as error:
            return ToolMessage(
                content=f"That tool call failed: {error}. Try another approach.",
                tool_call_id=request.tool_call["id"],
            )
            
class SupermarketEssentials(BaseModel):
    smarket: str = Field(description="The exact store name that was searched; it must match one of the provided store names exactly")
    prices: dict[str, Optional[Union[str, int, float]]] = Field(description="Item name to price. Keys must be exactly: milk_2L, cheese_1kg, mince_per_kg, eggs_10_pack. Use null if an item couldn't be found.")
    total_price: Optional[Union[str, int, float]] = Field(description="The total cost of the essentials at this supermarket, or null if incomplete")

class Essentials(BaseModel):
    region: str = Field(description="The region in which the prices are pulled from")
    supermarkets: Dict[str, SupermarketEssentials] = Field(description="Keyed by the exact store name from the provided store list, for example 'PAK'nSAVE Kilbirnie'")
    cheapest: str = Field(description="The exact store name of the cheapest total supermarket")
    
def format_essentials(essentials: Essentials) -> str:
    lines = [f"## Essentials comparison - {essentials.region}\n"]
    item_names = {"milk_2L": "Milk 2L", "cheese_1kg": "Cheese 1KG", "mince_per_kg": "Mince per kg", "eggs_10_pack": "Eggs (10 pack)"}
    for name, sm in essentials.supermarkets.items():
        lines.append(f"### {sm.smarket}")
        for item, price in sm.prices.items():
            lines.append(f"- **{item_names[item]}**: ${price if price else 'N/A'}\n")
        lines.append(f"**Total: ${sm.total_price if sm.total_price else 'N/A'}**\n")
    lines.append(f"---\n**Cheapest overall: {essentials.cheapest}**")
    return "\n".join(lines)

class Big3:
    def __init__(self):
        self.big3_id = str(uuid.uuid4())
        self.memory = InMemorySaver()
        self.tools = None
        self.worker = None
        
    async def setup(self):
        rate_limiter = InMemoryRateLimiter(
            requests_per_second=0.5,
            check_every_n_seconds=0.1,
            max_bucket_size=10
        )
        model = ChatOpenAI(
            model="gpt-5.4-mini",
            rate_limiter=rate_limiter
        )
        self.tools = await get_all_tools()
        self.worker = create_agent(
            model=model,
            tools=self.tools,
            system_prompt=f"{SYSTEM_PROMPT}\nToday is {datetime.now():%A %d %B %Y}.",
            middleware=[
                TolerateToolErrors(),
                TodoListMiddleware(),
                PIIMiddleware("email"), 
                PIIMiddleware("credit_card", apply_to_tool_results=True), 
                ModelCallLimitMiddleware(run_limit=30)
            ],
            checkpointer=self.memory,
            response_format=Essentials
        )
        
    async def get_prices(self, stores: list[str]):
        config = {"configurable": {"thread_id": f"big3-{uuid.uuid4()}"}}
        result = await self.worker.ainvoke({"messages": [{"role": "user", "content": f"Get the essentials from these New Zealand supermarket stores: {stores}. Find prices for all four items at each supermarket if possible. If an item is missing, only use null after trying multiple search variations and checking the site carefully."}]}, config)
        essentials: Essentials = result["structured_response"]
        return format_essentials(essentials)