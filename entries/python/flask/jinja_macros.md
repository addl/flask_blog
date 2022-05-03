
https://uniwebsidad.com/libros/explore-flask/chapter-8/creating-macros

## macro definition
Create a new html file where we will define our macro. i called this file "render_comment.html" and inside it the content is:
````html
{% macro render_comment(comment) %}

<div class="comment">
    <div class="picture">
        <img src="{{ comment.user.picture }}" width="50" height="50"/>
    </div>
    <div class="content">
        <div class="comment-header">
            <span>{{ comment.user.name }}</span>
        </div>
        <p>{{ comment.content | safe }}</p>
        <div class="actions">
            <a class="comment-reply" onclick="reply({{comment.id}})">{{ _('Reply') }}</a>
        </div>
    </div>
</div>

{% endmacro %}
````

## import and call
In order to call our brand new macro "render_comment" we need to import the html inside our templates, for example:
````html
{% from "macros/render_comment.html" import render_comment with context %}
````

Then we just call our macro:
````html
...
<div id="comments">
    {% for comment in post.comments %}
        {{ render_comment(comment) }}
    {% else %}
        <p>{{ _('Be the first in commenting on this post!') }}</p>
    {% endfor %}
</div>
...
````
