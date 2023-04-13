import json

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from News.models import NewsArticle


# ================================================== News article APIs ===============================
class GetNewsArticleDetails(APIView):
    http_method_names = ['get']
    def get(self,request):
        # Get request object and data from query parameters
        self.get_data = request.GET
        article_id = self.get_data.get("article_id",'')

        # Check if article_id is not provided and return all articles
        if not article_id:
            article_objs = NewsArticle.objects.filter(is_active=True).order_by('-created_at')
            article_dict = []
            for article in article_objs:
                # Construct dictionary for each article
                article_sub_dict = {}
                article_sub_dict['id'] = article.news_article_id
                article_sub_dict['name'] = article.name
                article_sub_dict['description'] = article.description
                article_sub_dict['author'] = article.author
                article_sub_dict['image_path'] = article.image_path
                article_sub_dict['source'] = article.source
                article_sub_dict['created_at'] = article.created_at.strftime("%Y-%m-%d %H:%M:%S")
                article_sub_dict['updated_at'] = article.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                article_sub_dict['is_active'] = article.is_active

                article_dict.append(article_sub_dict)
            # Return the list of articles as JSON response
            return Response(
                status=status.HTTP_200_OK,
                data={"article_data:": json.dumps(article_dict)},
                content_type='application/json'
            )

        # If article_id is provided, try to find the corresponding article
        try:
            article_objs = NewsArticle.objects.filter(news_article_id = article_id,is_active=True)
            if article_objs.exists():
                article_sub_dict = {}
                for article in article_objs:
                    # Construct dictionary for the found article
                    article_sub_dict['id'] = article.news_article_id
                    article_sub_dict['name'] = article.name
                    article_sub_dict['description'] = article.description
                    article_sub_dict['author'] = article.author
                    article_sub_dict['image_path'] = article.image_path
                    article_sub_dict['source'] = article.source
                    article_sub_dict['created_at'] = article.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    article_sub_dict['updated_at'] = article.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    article_sub_dict['is_active'] = article.is_active

                # Return the found article as JSON response
                return Response(
                    status=status.HTTP_200_OK,
                    data={json.dumps(article_sub_dict)},
                    content_type='application/json'
                )
            else:
                # Return 404 error if the article is not found
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error:": "News articles not found"},
                    content_type='application/json'
                )
        except Exception as error:
            # Return 500 error if there's any exception while trying to find the article
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"error:": "Internal Server Error: "},
                content_type='application/json'
            )

class CreateNewsArticle(APIView):
    # Only allow POST requests
    http_method_names = ['post']
    
    def post(self, request):
        # Get the POST data from the request
        self.post_data = request.POST
        
        # Check if POST data exists
        if self.post_data:
            # Get values from POST data
            article_name = self.post_data.get('name', '')
            description = self.post_data.get('description', '')
            author = self.post_data.get('author', '')
            image_path = self.post_data.get('image_path', '')
            source = self.post_data.get('source', '')
            
            try:
                # Use a database transaction to ensure data consistency
                with transaction.atomic():
                    # Create a dictionary of values to add to the NewsArticle object
                    article_to_add = {
                        'name': article_name,
                        'description': description,
                        'image_path': image_path,
                        'author': author,
                        'source': source
                    }
                    # Create a new NewsArticle object with the provided data
                    NewsArticle.objects.create(**article_to_add)
                    # Return a success response
                    return Response(
                        status=status.HTTP_200_OK,
                        data={"success:": "News article created successfully"},
                        content_type='application/json'
                    )
            except Exception as error:
                # Return an error response if there's an exception
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={"error:": "Internal Server Error"},
                    content_type='application/json'
                )
        else:
            # Return an error response if no POST data is provided
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error:": "Data not provided"},
                content_type='application/json'
            )

class RemoveNewsArticle(APIView):
    # Only allow POST requests
    http_method_names = ['post']
    
    def post(self, request):
        # Get the POST data from the request
        self.post_data = request.POST
        # Check if POST data exists
        if self.post_data:
            # Get the article ID from the POST data
            article_id = self.post_data.get('article_id', '')
            # If the article ID is not provided, return an error response
            if not article_id:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error:": "article id not found"},
                    content_type='application/json'
                )
            try:
                # Use a database transaction to ensure data consistency
                with transaction.atomic():
                    # Query the NewsArticle table for the article with the provided ID
                    article_objs = NewsArticle.objects.filter(news_article_id=article_id)
                    # If the article exists, mark it as inactive and save the changes
                    if article_objs.exists():
                        article_obj = article_objs.first()
                        article_obj.is_active = False
                        article_obj.save()
                        # Return a success response
                        return Response(
                            status=status.HTTP_200_OK,
                            data={"success:": "Removed News Article successfully"},
                            content_type='application/json'
                        )
                    else:
                        # If the article doesn't exist, return an error response
                        return Response(
                            status=status.HTTP_404_NOT_FOUND,
                            data={"error:": "News Article not found"},
                            content_type='application/json'
                        )
            except Exception as error:
                # If there's an exception, return an error response
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={"error:": "Internal Server Error"},
                    content_type='application/json'
                )
        else:
            # If no POST data is provided, return an error response
            return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error:": "Data not provided"},
                    content_type='application/json'
                )

class UpdateNewsArticle(APIView):
    """
    Update an existing news article.
    """
    http_method_names = ['post']

    def post(self, request):
        # Get the post data from the request
        post_data = request.POST

        if post_data:
            # Get the ID of the article to update
            article_id = post_data.get('news_article_id', '')

            if not article_id:
                # Return an error response if the article ID is not provided
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error:": "News article ID not found"},
                    content_type='application/json'
                )

            # Get the data to update the article with
            article_name = post_data.get('name', '')
            description = post_data.get('description', '')
            author = post_data.get('author', '')
            image_path = post_data.get('image_path', '')
            source = post_data.get('source', '')

            try:
                with transaction.atomic():
                    # Get the article to update
                    article_obj = get_object_or_404(NewsArticle, news_article_id=article_id)

                    # Update the article with the new data
                    article_obj.name = article_name
                    article_obj.description = description
                    article_obj.author = author
                    article_obj.image_path = image_path
                    article_obj.source = source
                    article_obj.save()

                    # Return a success response
                    return Response(
                        status=status.HTTP_200_OK,
                        data={"success:": "News article updated successfully"},
                        content_type='application/json'
                    )

            except Exception as error:
                # Return an error response if an exception occurs
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={"error:": "Internal Server Error"},
                    content_type='application/json'
                )

        else:
            # Return an error response if the post data is not provided
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error:": "Data not provided"},
                content_type='application/json'
            )
      
# ================================================== End =============================================