# luminagen_ai/reporting/report_generator.py
from jinja2 import Environment, FileSystemLoader
import os

def create_html_report(template_name: str, output_path: str, data: dict):
    """
    Generates a final HTML report by rendering a Jinja2 template with AI-generated data.
    """
    print("INFO: Generating final HTML report...")

    # Set up Jinja2 to look for templates in the project's root directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    # Render the template with our data dictionary
    html_content = template.render(data)

    # Write the final report to an HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"INFO: Report successfully generated at '{output_path}'")

