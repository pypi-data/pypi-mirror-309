import os
import argparse
import importlib.util
from datetime import datetime
import yaml
from .utils import read_markdown_file, read_markdown_directory
from .analyzer import analyze_markdown

def load_config():
    """
    Load configuration from the current working directory.
    Supports `config.py` or `config.yaml`.
    """
    config_path_py = os.path.join(os.getcwd(), "config.py")
    config_path_yaml = os.path.join(os.getcwd(), "config.yaml")

    if os.path.exists(config_path_py):
        # Load `config.py` dynamically
        spec = importlib.util.spec_from_file_location("config", config_path_py)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return {"endpoint": getattr(config, "API_ENDPOINT", ""), "api_key": getattr(config, "API_KEY", "")}

    elif os.path.exists(config_path_yaml):
        # Load `config.yaml`
        with open(config_path_yaml, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    return None

def main():
    parser = argparse.ArgumentParser(description="SEO Analyzer for Markdown Files using Huggingface API")
    parser.add_argument("input_path", help="Path to a Markdown file or directory")
    parser.add_argument("--api-key", help="API key for authentication (optional)", default=None)
    parser.add_argument("--endpoint", help="API endpoint URL (optional)", default=None)
    parser.add_argument("--batch", action="store_true", help="Process all Markdown files in a directory")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_path)
    batch_mode = args.batch

    # Load configuration from the working directory
    config = load_config()
    if not config:
        print("Error: No configuration file (config.py or config.yaml) found in the current directory.")
        return

    # Use config values or override with CLI arguments
    api_key = args.api_key or config.get("api_key", "")
    endpoint = args.endpoint or config.get("endpoint", "")

    if not endpoint or not api_key:
        print("Error: API endpoint or API key is missing. Please provide them in the config file or as CLI arguments.")
        return

    # Define the output directory for reports
    report_dir = os.path.join(os.getcwd(), "seo-report")
    os.makedirs(report_dir, exist_ok=True)

    if not os.path.exists(input_path):
        print(f"Error: The input path '{input_path}' does not exist.")
        return

    if batch_mode and os.path.isdir(input_path):
        # Batch processing
        print("Processing directory in batch mode...")
        markdown_files = read_markdown_directory(input_path)
        for file_name, content in markdown_files:
            print(f"Analyzing {file_name}...")
            try:
                analysis_result = analyze_markdown(content, api_key, endpoint)
                save_markdown_report(file_name, analysis_result, report_dir)
            except RuntimeError as e:
                print(f"Error analyzing {file_name}: {e}")
    elif os.path.isfile(input_path):
        # Single file processing
        print(f"Analyzing {input_path}...")
        try:
            content = read_markdown_file(input_path)
            analysis_result = analyze_markdown(content, api_key, endpoint)
            save_markdown_report(os.path.basename(input_path), analysis_result, report_dir)
        except RuntimeError as e:
            print(f"Error: {e}")
    else:
        print("Error: Please specify a valid file or directory.")

def save_markdown_report(file_name, analysis_result, report_dir, language="vi"):
    """
    Save the analysis result to a well-formatted Markdown file with improved readability and bilingual support.

    :param file_name: Name of the file being analyzed.
    :param analysis_result: Analysis results from the API.
    :param report_dir: Directory to save the report.
    :param language: Language of the report ('vi' for Vietnamese, 'en' for English).
    """
    translations = {
        "en": {
            "report_title": "📝 SEO Analysis Report",
            "file": "File",
            "generated_on": "Generated On",
            "summary": "🔍 Summary",
            "detailed_analysis": "📋 Detailed Analysis",
            "title_length": "Title Length",
            "description_length": "Description Length",
            "keyword_density": "Keyword Density",
            "found_headings": "Found Headings",
            "missing_headings": "Missing Headings",
            "internal_links": "Internal Links",
            "outbound_links": "Outbound Links",
            "contains_multimedia": "Contains Multimedia",
            "yes": "Yes",
            "no": "No",
            "metric": "Metric",
            "value": "Value",
            "true": "True",
            "false": "False",
            "good": "Good",
            "out_of_range": "Out of Range",
            "slug_length": "Slug Length",
            "keyword_in_title": "Keyword in Title",
            "length_status": "Length Status",
            "average_paragraph_length": "Average Paragraph Length",
            "positive_words": "Positive Words",
            "negative_words": "Negative Words",
            "power_words": "Power Words",
            "word_count_score": "Word Count Score",
            "main_keyword_unique": "Main Keyword Unique",
        },
        "vi": {
            "report_title": "📝 Báo Cáo Phân Tích SEO",
            "file": "Tệp",
            "generated_on": "Thời Gian Tạo",
            "summary": "🔍 Tóm Tắt",
            "detailed_analysis": "📋 Phân Tích Chi Tiết",
            "title_length": "Độ Dài Tiêu Đề",
            "description_length": "Độ Dài Mô Tả",
            "keyword_density": "Mật Độ Từ Khoá",
            "found_headings": "Các Tiêu Đề Tìm Thấy",
            "missing_headings": "Các Tiêu Đề Thiếu",
            "internal_links": "Liên Kết Nội Bộ",
            "outbound_links": "Liên Kết Bên Ngoài",
            "contains_multimedia": "Chứa Nội Dung Đa Phương Tiện",
            "yes": "Có",
            "no": "Không",
            "metric": "Chỉ Số",
            "value": "Giá Trị",
            "true": "Có",
            "false": "Không",
            "good": "Tốt",
            "out_of_range": "Ngoài khoảng",
            "slug_length": "Độ Dài Slug",
            "keyword_in_title": "Từ Khoá Trong Tiêu Đề",
            "length_status": "Trạng Thái Độ Dài",
            "average_paragraph_length": "Độ Dài Đoạn Văn Trung Bình",
            "positive_words": "Từ Tích Cực",
            "negative_words": "Từ Tiêu Cực",
            "power_words": "Từ Mạnh",
            "word_count_score": "Điểm Số Từ",
            "main_keyword_unique": "Từ Khoá Chính Duy Nhất",
            "keyword_in_url": "Từ Khoá Trong URL",
            "word_count": "Số Từ",
            "keyword_count": "Số Từ Khoá",
            "slug": "Đường dẫn url (slug)",
            "density_status": "Trạng Thái Mật Độ",
            "found_levels": "Tìm thấy trong các cấp tiêu đề:",
            "missing_levels": "Thiếu trong các cấp tiêu đề:",
            "keyword_in_alt": "Từ Khoá Trong thẻ alt",
            "outbound_links_count": "Số Liên Kết Bên Ngoài",
            "internal_links_count": "Số Liên Kết Nội Bộ",
            "title": "Tiêu Đề",
            "description": "Mô Tả",
            "headings": "Tiêu Đề",
            "image_alt": "Thuộc tính mô tả ảnh",
            "links": "Liên Kết",
            "paragraph_length": "Độ Dài Đoạn Văn",
            "title_word_type": "Loại Từ Trong Tiêu Đề",
        },
    }

    t = translations.get(language, translations["vi"])  # Default to Vietnamese
    sanitized_file_name = os.path.splitext(file_name)[0].replace(" ", "_").replace("/", "_")
    report_path = os.path.join(report_dir, f"{sanitized_file_name}_seo_report.md")

    def translate_value(value):
        """Translate boolean and common statuses."""
        if isinstance(value, bool):
            return t["true"] if value else t["false"]
        if isinstance(value, str):
            return t.get(value.lower(), value)
        if isinstance(value, list):
            return ", ".join([translate_value(v) for v in value])  # Recursively translate lists
        return value

    with open(report_path, "w", encoding="utf-8") as f:
        # Title and Metadata
        f.write(f"# {t['report_title']}\n\n")
        f.write(f"**{t['file']}:** `{file_name}`\n\n")
        f.write(f"**{t['generated_on']}:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        # Summary Section
        f.write(f"## {t['summary']}\n")
        summary_items = [
            (t["title_length"], f"{analysis_result['title']['title_length']} ({translate_value(analysis_result['title']['length_status'])})"),
            (t["description_length"], f"{analysis_result['description']['description_length']} ({translate_value(analysis_result['description']['length_status'])})"),
            (t["keyword_density"], f"{round(analysis_result['keyword_density']['keyword_density'], 2)}% ({translate_value(analysis_result['keyword_density']['density_status'])})"),
            (t["found_headings"], translate_value(analysis_result['headings']['found_levels'])),
            (t["missing_headings"], translate_value(analysis_result['headings']['missing_levels'])),
            (t["internal_links"], analysis_result['links']['internal_links_count']),
            (t["outbound_links"], analysis_result['links']['outbound_links_count']),
            (t["contains_multimedia"], translate_value(analysis_result.get("contains_multimedia"))),
        ]

        for item, value in summary_items:
            f.write(f"- **{item}:** {value}\n")
        f.write("\n---\n\n")

        # Detailed Sections
        f.write(f"## {t['detailed_analysis']}\n")
        for section, details in analysis_result.items():
            human_readable_section = t.get(section, section.replace("_", " ").capitalize())
            f.write(f"### {human_readable_section}\n")
            if isinstance(details, dict):
                # Use a table format for better readability
                f.write(f"| {t['metric']} | {t['value']} |\n")
                f.write("|--------|-------|\n")
                for key, value in details.items():
                    human_readable_key = t.get(key, key.replace("_", " ").capitalize())
                    value = translate_value(value)
                    f.write(f"| **{human_readable_key}** | {value} |\n")
            else:
                f.write(f"{details}\n")
            f.write("\n---\n\n")

    print(f"✨ Báo cáo đã được lưu tại: {report_path}" if language == "vi" else f"✨ Report saved to: {report_path}")


if __name__ == "__main__":
    main()
