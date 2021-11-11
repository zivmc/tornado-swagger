import tornado.ioloop
import tornado.options
import tornado.web

from tornado_swagger.model import register_swagger_model
from tornado_swagger.setup import setup_swagger


class PostsHandler(tornado.web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - Posts
        summary: List posts
        description: List all posts in feed
        responses:
            200:
              description: list of posts
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      $ref: '#/components/schemas/PostModel'
        """

    def post(self):
        """
        ---
        tags:
        - Posts
        summary: Add posts
        description: Add posts in feed
        requestBody:
          description: post data
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostModel'
        """


class PostsDetailsHandler(tornado.web.RequestHandler):
    def get(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Get posts details
        description: posts full version
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to return
            required: true
            type: string
        responses:
            200:
              description: list of posts
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      $ref: '#/components/schemas/PostModel'
        """

    def patch(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Edit posts
        description: Edit posts details
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to edit
            required: true
            type: string
        requestBody:
          description: post data
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostModel'
        """

    def delete(self, posts_id):
        """
        ---
        tags:
        - Posts
        summary: Delete posts
        description: Remove posts from feed
        parameters:
        -   name: posts_id
            in: path
            description: ID of post to delete
            required: true
            type: string
        """


@register_swagger_model
class PostModel:
    """
    ---
    type: object
    description: Post model representation
    properties:
        id:
            type: integer
            format: int64
        title:
            type: string
        text:
            type: string
        is_visible:
            type: boolean
            default: true
    """


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(r"/api/posts", PostsHandler),
        tornado.web.url(r"/api/posts/(\w+)", PostsDetailsHandler),
        tornado.web.url(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/var/www"}),
    ]

    def __init__(self):
        settings = {"debug": True}

        setup_swagger(
            self._routes,
            swagger_url="/doc",
            api_base_url="/",
            description="",
            api_version="1.0.0",
            title="Journal API",
            contact="name@domain",
            schemes=["https"],
            security_definitions={"ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"}},
        )
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":
    tornado.options.define("port", default="8080", help="Port to listen on")
    tornado.options.parse_command_line()

    app = Application()
    app.listen(port=8080)

    tornado.ioloop.IOLoop.current().start()
