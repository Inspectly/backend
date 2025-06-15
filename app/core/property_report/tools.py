REPORT_RESPONSE_TOOL = {
    'type': 'function',
    'function': {
        'name': 'generate_report_response',
        'description': 'Generates a structured report with categorized issue types and their details from a md file that was created from an inspection report.',
        'parameters': {
            'type': 'object',
            'properties': {
                'IssueTypes': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'type': {
                                'type': 'string',
                                'description': 'The category or type of issue (e.g., Roofing, Plumbing).'
                            },
                            'descriptions': {
                                'type': 'string',
                                'description': 'General description for this issue type.'
                            },
                            'issues': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {
                                            'type': 'string',
                                            'description': 'Name of the individual issue.'
                                        },
                                        'description': {
                                            'type': 'string',
                                            'description': 'Detailed description of the issue.'
                                        },
                                    },
                                    'required': ['name', 'description']
                                }
                            }
                        },
                        'required': ['type', 'descriptions', 'issues']
                    }
                }
            },
            'required': ['IssueTypes']
        }
    }
}