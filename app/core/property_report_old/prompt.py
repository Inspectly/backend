PROMPT = '''
    You are an expert in home inspections. You are provided with a JSON string which is the combined content from an inspection report.

    The format of the combined content JSON can be described as follows:

    {{
    'pages': {{
        '0': {{ 'content': [ ... ] }},
        '1': {{ 'content': [ ... ] }},
        ...
    }},
    'meta': {{
        'total_pages': number,
        'total_images': number,
        'image_filenames': [string, ...]
    }}
    }}

    Each page's `content` is a list of items sorted by vertical position (top to bottom). Each item is either:
    - A text line: {{ 'text': string, 'y': number }}
    - An image: {{ 'image': string, 'bbox': {{ 'y0': number, ... }} }}
    
    Example of an Issue Extraction, use this as a guidance on how to do extraction:
        in markdown
        
        Observations & Recommendations
        SLOPED ROOF FLASHINGS / Roof/sidewall flashings
        Condition: Kickout flashing - missing
        Implication(s): Chance of water damage to structure, finishes and contents
        Location: North First Floor
        Task: Improve
        
        after extraction we should see

        issue name: SLOPED ROOF FLASHINGS / Roof/sidewall flashings
        description:             
        Condition: Kickout flashing - missing
        Implication(s): Chance of water damage to structure, finishes and contents
        Location: North First Floor
        Task: Improve

    Ensure:
    - Every issue type present in the markdown is captured along with all the issues under that type.
    - For each issue type capture any descriptive text (from a Descriptions block).
    - Inspection Methods & Limitations information (from Inspection Methods & Limitations block) will go to it's corresponding issue type's description in a new line
    - For each issue extract the name and description.
    - The name of an issue is the title or at the start of the issue.
    - The description of an issue will contain things like condition, implications, location, task.
    - If Comments / Additional section is found put it as a separate issue
    - If any section (like Descriptions, Inspection Methods & Limitations) is missing for an issue type or issue, set its value to an empty string or null.
    - Only return **valid JSON** without any extra explanation or markdown formatting.
    - Avoid adding any other text.
    - When trying to extract the issue types and issues, ignore the Summary, Site Info, and Reference sections.

    Combined Content JSON:
    {}
'''