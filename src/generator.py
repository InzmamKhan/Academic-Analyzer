import os
import webbrowser
from jinja2 import Environment, FileSystemLoader

def render_report(analytics_data: dict, template_dir: str, output_path: str):
    """
    Takes processed statistics and student data, applies it to a Jinja2 
    HTML template, and writes a self-contained web report to disk.
    """
    # 1. Initialize Jinja2 environment pointing to the templates directory
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Templates directory not found at: {template_dir}")
        
    env = Environment(loader=FileSystemLoader(template_dir))
    
    try:
        # Load the core layout template
        template = env.get_template("dashboard.html")
    except Exception as e:
        raise FileNotFoundError(f"Could not load template 'dashboard.html'. Details: {e}")

    # 2. Render the variables into the HTML blueprint
    # We unpack everything inside analytics_data directly into the template context
    html_content = template.render(
        class_metrics=analytics_data["class_metrics"],
        component_metrics=analytics_data["component_metrics"],
        at_risk_students=analytics_data["at_risk_students"],
        student_data=analytics_data["student_data"]
    )

    # 3. Write out the compiled static HTML report
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n🚀 [SUCCESS] HTML Report generated successfully!")
    print(f"📂 Saved to: {os.path.abspath(output_path)}")
    
    # 4. Open automatically in the user's default browser
    webbrowser.open(f"file://{os.path.abspath(output_path)}")