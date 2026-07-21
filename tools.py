from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import GoogleSerperRun
from langchain_core.tools import tool

load_dotenv(override=True)

@tool
def find_store_item_name(store: str, item: str):
    """Find the correct item name depending on the store being searched.

    Accepts short keys such as Pak, New, Wol, or full store names like PAK'nSAVE,
    New World, and Woolworths.
    """
    item_names = {
        "Pak": {
            "milk": "Pams Value Standard Milk 2l",
            "mince": "NZ Beef Mince",
            "cheese": "Pams Value Cheese 1kg",
            "eggs": "Woodland Free Range Size 6 Eggs 10pk",
        },
        "New": {
            "milk": "Value Standard Milk 2l",
            "mince": "Prime Beef Mince kg",
            "cheese": "Pams Value Cheese 1kg",
            "eggs": "Woodland Free Range Size 6 Eggs 10pk",
        },
        "Wol": {
            "milk": "Woolworths Milk Standard 2L",
            "mince": "Woolworths Beef Mince Value Tray Min Order 450g",
            "cheese": "Woolworths Cheese Cheddar Everyday",
            "eggs": "Woodland Eggs Free Range Size 7 10pack",
        },
    }

    store_key = str(store or "").strip().lower()
    item_key = str(item or "").strip().lower()

    if store_key in {"pak", "pak'nsave", "paknsave", "pams"}:
        store_key = "Pak"
    elif store_key in {"new", "new world", "newworld"}:
        store_key = "New"
    elif store_key in {"wol", "woolworths", "woolworths nz"}:
        store_key = "Wol"
    else:
        store_key = str(store or "").strip()

    if store_key not in item_names:
        return None

    return item_names[store_key].get(item_key)
    
async def get_all_tools():
    """Return the full tool list"""     
    search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())
    client = MultiServerMCPClient(
        {
            "playwright": {
                "transport": "stdio",
                "command": "npx",
                "args": ["@playwright/mcp@latest", "--isolated"]
            }
        }
    )
    mcp_tools = await client.get_tools()
    
    ALLOWED_TOOLS = {
    "browser_navigate",
    "browser_snapshot",   # or browser_get_text / accessibility tree tool
    "browser_click",
    "browser_wait_for",
    "browser_take_screenshot",  # optional, for debugging
    }

    mcp_tools = [t for t in mcp_tools if t.name in ALLOWED_TOOLS]
    tools = [search, find_store_item_name] + mcp_tools
    return tools

