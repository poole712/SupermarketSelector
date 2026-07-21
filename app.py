import html
import gradio as gr

import styles
from big3 import Big3

LAUNCH_STYLE = {"css": styles.CSS}

LOGO = """
<div class="app-header">
        <div class="brand-mark" aria-label="Brand mark">
            <div class="brand-dot brand-green"></div>
            <div class="brand-dot brand-yellow"></div>
            <div class="brand-dot brand-red"></div>
        </div>
        <div class="app-title-text">Supermarket Selector</div>
    </div>
"""
async def setup():
    big3 = Big3()
    await big3.setup()
    return big3, gr.update(interactive=True)

async def process_compare(big3, region: str):
    store_map = {"Auckland": ["PAK'nSAVE Mt Albert", "New World Mt Roskill", "Woolworths Mt Eden"],
                 "Wellington": ["PAK'nSAVE Kilbirnie", "New World Newtown", "Woolworths Kilbirnie"],
                 "Christchurch": ["PAK'nSAVE Moorhouse", "New World Prestons", "Woolworths Moorhouse Ave"],
                 "Dunedin": ["PAK'nSAVE Dunedin", "New World Centre City", "Woolworths Dunedin Central"]}
    if big3 is None:
        return big3
    results = await big3.get_prices(store_map[region])
    return results

with gr.Blocks(title="Big3") as ui:
    
    gr.HTML(LOGO, elem_id="app-title")
    big3 = gr.State()
    gr.HTML(value="""<div class='warning'><p>Welcome to <b>Supermarket Selector</b>. 
            This app allows you to easily view which Supermarkets offers the best value for your essential grocery items.<br>
            <b>Warning:</b> results can vary depending on agent accuracy and timeouts.</p></div>""", elem_id="warning")
    with gr.Row():
        results = gr.Markdown("results...", height=325, elem_id="results-box", )
    with gr.Column():
        with gr.Group(elem_id="region-wrapper"):
            region = gr.Dropdown(
                value="Auckland",
                label="Region:",
                choices=["Auckland", "Wellington", "Christchurch", "Dunedin"],
                elem_id="region-dropdown",
            )
            submit_button = gr.Button("Submit", elem_id="submit-btn", interactive=False)

    
    ui.load(setup, [], [big3, submit_button])
    submit_button.click(process_compare, [big3, region], [results])
    

if __name__ == "__main__":
    ui.launch(inbrowser=True, **LAUNCH_STYLE)