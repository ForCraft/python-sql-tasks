import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO posts (title, content, author_id)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (post['title'], post['content'], post['author_id']))
        post_id = cur.fetchone()[0]
    conn.commit()
    return post_id

def add_comment(conn, comment):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (comment['post_id'], comment['author_id'], comment['content']))
        comment_id = cur.fetchone()[0]
    conn.commit()
    return comment_id

def get_latest_posts(conn, n):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        # Get n latest posts ordered by created_at DESC
        cur.execute("""
            SELECT id, title, content, author_id, created_at
            FROM posts
            ORDER BY created_at DESC
            LIMIT %s
        """, (n,))
        posts = cur.fetchall()
        result = []
        for post in posts:
            # Get comments for this post, ordered by created_at ASC
            cur.execute("""
                SELECT id, author_id, content, created_at
                FROM comments
                WHERE post_id = %s
                ORDER BY created_at ASC
            """, (post['id'],))
            comments = cur.fetchall()
            post_dict = {
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'author_id': post['author_id'],
                'created_at': post['created_at'],
                'comments': [
                    {
                        'id': c['id'],
                        'author_id': c['author_id'],
                        'content': c['content'],
                        'created_at': c['created_at'],
                    }
                    for c in comments
                ]
            }
            result.append(post_dict)
        return result

# END
