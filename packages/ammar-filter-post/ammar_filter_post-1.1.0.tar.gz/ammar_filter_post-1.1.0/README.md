# filteration-post

A Python package to retrieve all posts from a DynamoDB table and return them sorted by likes in descending order.

## Build and Upload the Package to PyPI
ßßß
### **Prerequisites**

- Install `twine` and `wheel` `setuptools`:

  ```bash
  pip install twine wheel setuptools

### **Build the Package**
In the root directory (ammar_filter_post/), run:

```bash
    python setup.py sdist bdist_wheel
```

Upload to PyPI First, create an account on PyPI if you haven't already.

```bash
    twine upload dist/*
```
You will be prompted to enter your PyPI username and password.
## How to install the Library

```bash
pip install ammar_filter_post
```

## How to use the Library
```bash
    import boto3
    from ammar_filter_post import get_posts_sorted_by_likes

    # Replace 'your-region' and 'YourTableName' with your actual AWS region and DynamoDB table name
    dynamodb = boto3.resource('dynamodb', region_name='your-region')
    table = dynamodb.Table('YourTableName')

    sorted_posts = get_posts_sorted_by_likes(table)

    for post in sorted_posts:
        print(post)
```