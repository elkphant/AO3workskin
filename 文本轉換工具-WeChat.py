import tkinter as tk
import pyperclip

def convert_text():
	input_text = input_textbox.get("1.0", "end").strip()
	right_role = right_role_entry.get().strip()
	group_format = group_var.get()
	output_text = add_html_tags(input_text, right_role, group_format)
	output_textbox.delete("1.0", "end")
	output_textbox.insert("1.0", output_text)

def copy_output():
	output_text = output_textbox.get("1.0", "end").strip()
	pyperclip.copy(output_text)

def add_html_tags(text, right_role, group_format):
	lines = text.split('\n')
	html_output = ''
	for i, line in enumerate(lines):
		if '：' in line:  # 全形冒號分隔[角色名稱]與[文本]
			role, rest = line.split('：', 1)
			role_span = f'<span class="hide">{role}：</span>'
			if role == right_role:  # 判別是否等同輸入的主視角名稱
				role_tag = 'right'
			else:
				role_tag = 'left'
			if role_tag == 'right':  # 插入HTML標籤
				html_output += f'<p class="{role_tag}">{role_span}{rest}</p>\n'
			elif group_format == "私聊":
				html_output += f'<p class="{role_tag}">{role_span}{rest}</p>\n'
			elif group_format == "群聊":
				html_output += f'<p class="sender">{role}<span class="hide">：</span><span class="{role_tag}">{rest}</span></p>\n'
		else:
			if i == 0:  # 第一行使用 header
				html_output += f'<p class="header">{line}</p>\n'
			else:  # 其他使用 caption
				html_output += f'<p class="caption">{line}</p>\n'
	html_output = '<div class="wechat">\n' + html_output + '</div>\n'
	return html_output

# GUI setup
root = tk.Tk()
root.title("文本轉換工具")

# Frame for top controls
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x", padx=10, pady=10)

group_label = tk.Label(top_frame, text="文本格式：")
group_label.pack(side="left", padx=(0, 10))

group_var = tk.StringVar()
group_var.set("私聊")
group_options = ["私聊", "群聊"]
group_menu = tk.OptionMenu(top_frame, group_var, *group_options)
group_menu.pack(side="left", padx=(0, 10))

right_role_label = tk.Label(top_frame, text="主視角名稱：")
right_role_label.pack(side="left", padx=(0, 10))

right_role_entry = tk.Entry(top_frame, width=10)
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

input_textbox = tk.Text(input_output_frame, width=20)
input_textbox.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 5))

output_textbox = tk.Text(input_output_frame, width=20)
output_textbox.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 5))

root.mainloop()
