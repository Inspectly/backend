import pymupdf

class Report_Parser:
    def __init__(self):
        pass
    
    def extract_lines_y(self, pdf_content: bytes):
        doc = pymupdf.open(stream = pdf_content, filetype = 'pdf')
        result_lines = []

        for page_num, page in enumerate(doc):
            words = page.get_text('words')  # (x0, y0, x1, y1, text, block_no, line_no, word_no)
            lines = {}

            for word in words:
                x0, y0, x1, y1, text, *_ = word
                line_key = round(y0)

                if line_key not in lines:
                    lines[line_key] = []
                lines[line_key].append((x0, text))  # store by x0 to preserve word order

            for y_coord in sorted(lines.keys()):
                sorted_words = sorted(lines[y_coord], key=lambda w: w[0])
                line_text = ' '.join([w[1] for w in sorted_words])
                result_lines.append({
                    'text': line_text,
                    'y': y_coord,
                    'page': page_num
                })

        doc.close()
        return result_lines
    
    def extract_combined_content(self, file_content: str, report_name: str) -> dict:
        text_lines = self.extract_lines_y(file_content)

        combined_by_page = {}

        # Process text lines
        for item in text_lines:
            page = str(item['page'])
            y = int(item['y'])
            text = item['text']
            combined_by_page.setdefault(page, []).append({
                'text': text,
                'y': y
            })

        def get_y(item):
            if 'y' in item:
                return item['y']
            elif 'bbox' in item:
                return item['bbox']['y0']
            return 0

        for page in combined_by_page:
            combined_by_page[page] = sorted(combined_by_page[page], key=get_y)

        total_pages = len(combined_by_page)

        return {
            'report_name': report_name,
            'pages': {page: {'content': content} for page, content in combined_by_page.items()},
            'meta': {
                'total_pages': total_pages
            }
        }
    