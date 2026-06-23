import os
import webbrowser
from jinja2 import Environment, FileSystemLoader

def render_report(analytics_data: dict, template_dir: str, output_path: str):
    """
    Takes processed statistics and student data, applies it to a Jinja2 
    HTML template, injects the CSS directly, and writes a self-contained web report.
    """
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Templates directory not found at: {template_dir}")
        
    env = Environment(loader=FileSystemLoader(template_dir))
    
    try:
        template = env.get_template("dashboard.html")
    except Exception as e:
        raise FileNotFoundError(f"Could not load template 'dashboard.html'. Details: {e}")

    # --- NEW FEATURE: Read the CSS file directly ---
    css_path = os.path.join(template_dir, "styles.css")
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
    else:
        print(f"⚠️ Warning: styles.css not found at {css_path}. Report will lack styling.")

    # Render variables AND the raw CSS string into the template context
    html_content = template.render(
        class_metrics=analytics_data["class_metrics"],
        component_metrics=analytics_data["component_metrics"],
        at_risk_students=analytics_data["at_risk_students"],
        student_data=analytics_data["student_data"],
        embedded_css=css_content  # <-- Passing the CSS here
    )

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n🚀 [SUCCESS] Self-contained HTML Report generated successfully!")
    print(f"📂 Saved to: {os.path.abspath(output_path)}")
    
    webbrowser.open(f"file://{os.path.abspath(output_path)}")