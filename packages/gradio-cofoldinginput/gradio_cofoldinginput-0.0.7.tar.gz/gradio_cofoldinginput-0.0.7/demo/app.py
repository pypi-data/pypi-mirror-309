
import gradio as gr
from gradio_cofoldinginput import CofoldingInput

import json


def predict(input):
    input = json.dumps(input)
    return input

with gr.Blocks() as demo:
    jobname = gr.Textbox(label="Job Name")
    inp=CofoldingInput(label="Input")

    preinput =  {"chains": [
        {
            "class": "DNA",
            "sequence": "ATGCGT",
            "chain": "A"
        },
        {
            "class": "protein",
            "sequence": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "chain": "B"
        },
        {
            "class": "ligand",
            "name": "ZN",
            "smiles": "",
            "sdf": "",
            "chain": "C"
        },
        {
            "class": "ligand",
            "smiles": "CCCCCCCCCCCCCCCCCCCC",
            "name": "",
            "sdf": "",
            "chain": "D"
        }
    ], "covMods":[]
    }
    # inp2=CofoldingInput(preinput, label="Input prefilled")
    btn = gr.Button("Submit")
    out = gr.HTML()

    gr.Examples([["test",preinput]], inputs=[jobname,inp])

    btn.click(predict, inputs=[inp], outputs=[out])

if __name__ == "__main__":
    demo.launch()
