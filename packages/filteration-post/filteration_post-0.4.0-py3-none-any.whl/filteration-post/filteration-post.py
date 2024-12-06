def get_posts_sorted_by_likes(table):
    """
    Retrieve all posts from the DynamoDB table and sort them by likes in descending order.

    :param table: DynamoDB Table resource.
    :return: List of posts sorted by likes.
    """
    try:
        # Scan the table to retrieve all items
        response = table.scan()
        items = response.get('Items', [])

        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        # Sort items by 'likes' in descending order
        sorted_items = sorted(items, key=lambda x: x.get('likes', 0), reverse=True)
        return sorted_items

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
