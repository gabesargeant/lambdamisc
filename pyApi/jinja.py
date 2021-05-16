
from jinja2 import Template

template = """
<html>
<head>
<title>{{ requestObj }}</title>
</head>
<body>
<table>
<tr><th>LastModified</th><th>Size</th><th>Key</th></tr>
{% for item in data %}
<tr><td>{{ item['LastModified'] }} </td><td>  {{ item['Size'] }} </td><td> {{ item['Key'] }}</td></tr>
{% endfor %}
</table>
</body>
<html>
"""

data = [
    {"LastModified": "---", "Key": "folder1/folder10/", "Size": "dir"}, 
    {"LastModified": "---", "Key": "folder1/folder11/", "Size": "dir"}, 
    {"LastModified": "05/16/2021, 10:41:29", "Key": "folder1/data3.csv", "Size": 2400445}, 
    {"LastModified": "05/16/2021, 10:41:29", "Key": "folder1/data4.csv", "Size": 25520043}
]

print(data)

j2_template = Template(template)

print(j2_template.render(data=data))

