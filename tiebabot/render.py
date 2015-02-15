import os
from jinja2 import FileSystemLoader, Environment

cwd = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(cwd, 'templates')
ENV = Environment(loader=FileSystemLoader(template_dir))


def render(template_name, **kwargs):
    template = ENV.get_template(template_name)
    return template.render(**kwargs)


def render_to_file(template_name, target_file, **kwargs):
    content = render(template_name, **kwargs)
    with open(target_file, 'w') as f:
        f.write(content.encode('utf8'))


if __name__ == '__main__':
    print render('base.html', title='hehe')
