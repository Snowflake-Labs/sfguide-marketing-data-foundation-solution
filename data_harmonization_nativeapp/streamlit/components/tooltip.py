
def tooltip_component(text: str) -> str:
    return f'''
    <div class="tooltip-container">
        <span class="tooltip-text">{text}</span>
        <div class="tooltip-tail tooltip-tail-bg"></div>
        <div class="tooltip-tail tooltip-tail-border"></div>
    </div>
    '''


def tooltip_stylesheet() -> str:
    return f'''
    <style>
        .tooltip {{
            z-index: 1;
        }}
        
        .tooltip-container {{
            width: fit-content;
            visibility: hidden;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            overflow-wrap: anywhere;
            background-color: #F0F2F6;
            box-shadow: 0 0 2px 0px #555;

            /* Position the tooltip */
            position: absolute;
            top: 30px;
            z-index: 1;
        }}

        .tooltip:hover .tooltip-container {{
            visibility: visible;
        }}

        .tooltip-text {{
            font-size: 12px;
            font-weight: 400;
        }}

        .tooltip-tail {{
            position: absolute;
            width: 0;
            height: 0;
            left: 20px;
            border-width: 10px;
            border-style:solid;
            transform: rotate(180deg);
        }}

        .tooltip-tail-bg {{
            top: -20px;
            border-color: #5555555c transparent transparent transparent;
        }}

        .tooltip-tail-border {{
            position: absolute;
            top: -18px;
            border-color: #F0F2F6 transparent transparent transparent;
        }}
    </style>
    '''
