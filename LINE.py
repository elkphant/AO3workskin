import tkinter as tk
import pyperclip

def convert_text():
	input_text = input_textbox.get("1.0", "end").strip()
	right_role = right_role_entry.get().strip()
	selected_group_format = group_var.get()
	output_text = add_html_tags(input_text, right_role, selected_group_format)
	output_textbox.delete("1.0", "end")
	output_textbox.insert("1.0", output_text)

def copy_output():
	output_text = output_textbox.get("1.0", "end").strip()
	pyperclip.copy(output_text)

def add_html_tags(text, right_role, group_format):
	lines = text.split('\n')
	html_output = ''
	for i, line in enumerate(lines):
		if '：' in line:
			role, rest = line.split('：', 1)
			if ' ' in rest:
				message_content, timestamp, *readreceipt = rest.split(' ')
				readreceipt = ' '.join(readreceipt)
			else:
				message_content = rest
				timestamp = ''
				readreceipt = ''
			if role == right_role:
				role_tag = 'right'
			else:
				role_tag = 'left'
			role_span = f'<span class="hide">{role}：</span>'
			message_span = f'{message_content}'
			timestamp_span = f'<span class="timestamp">{timestamp}</span>' if timestamp else ''
			readreceipt_span = f'<span class="readreceipt">{readreceipt}</span>' if readreceipt else ''
			if role_tag == 'right':
				html_output += f'<p class="{role_tag}">{role_span}{message_span}{timestamp_span}{readreceipt_span}</p>\n'
			elif group_format == "私訊":
				html_output += f'<p class="left">{role_span}{message_span}{timestamp_span}{readreceipt_span}</p>\n'
			elif group_format == "群組":
				html_output += f'<p class="left group"><span class="member">{role}</span><span class="hide">：</span>{message_span}{timestamp_span}{readreceipt_span}</p>\n'
		else:
			if i == 0:  # 第一行使用 header
				html_output += f'<p class="header">{line}</p>\n'
			else:
				html_output += f'<p class="caption">{line}</p>\n'
	html_output = '<div class="line">\n' + html_output + '</div>\n'
	return html_output

# GUI setup
root = tk.Tk()
root.title("文本轉換工具")

# Frame for top controls
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x", padx=10, pady=10)

group_label = tk.Label(top_frame, text="選擇文本格式：")
group_label.pack(side="left", padx=(0, 10))

group_var = tk.StringVar()
group_var.set("私訊")
group_options = ["私訊", "群組"]
group_menu = tk.OptionMenu(top_frame, group_var, *group_options)
group_menu.pack(side="left", padx=(0, 10))

right_role_label = tk.Label(top_frame, text="主視角名稱：")
right_role_label.pack(side="left", padx=(0, 10))

right_role_entry = tk.Entry(top_frame, width=20)
right_role_entry.pack(side="left", padx=(0, 10))

convert_button = tk.Button(top_frame, text="轉換", command=convert_text)
convert_button.pack(side="left", padx=(0, 10))

copy_button = tk.Button(top_frame, text="複製", command=copy_output)
copy_button.pack(side="left", padx=(0, 10))

# Frame for input and output labels
label_frame = tk.Frame(root)
label_frame.pack(side="top", fill="x", padx=10, pady=(0, 5))

input_label = tk.Label(label_frame, text="轉換前：")
input_label.pack(side="left", expand=True, anchor="w")

output_label = tk.Label(label_frame, text="轉換後：")
output_label.pack(side="left", expand=True, anchor="w")

# Frame for input and output textboxes
input_output_frame = tk.Frame(root)
input_output_frame.pack(expand=True, fill="both", padx=10, pady=0)

input_textbox = tk.Text(input_output_frame)
input_textbox.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 5))

output_textbox = tk.Text(input_output_frame)
output_textbox.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 5))



root.mainloop()
