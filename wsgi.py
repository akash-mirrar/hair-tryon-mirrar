# from mirrar_hair_tryon import create_app
from app import create_app

# if __name__ == '__main__':
#     from parser import align_parser, param_parser
#     app = create_app(align_parser, param_parser)
#     app.run(host="0.0.0.0", port=5000, debug=True)
# else:
#     from parser import align_parser, param_parser
#     gunicorn_app = create_app(align_parser, param_parser)
#     gunicorn_app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    from parser import *
    app = create_app(align_parser, param_parser)
    print(app.url_map)
    app.run()