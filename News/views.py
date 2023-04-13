import datetime
import hashlib
import json
import os
import random
import string

import requests
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from NewsApplication.settings import ATTACHMENTS_PATH, HOSTNAME




class NewsDashboard(View):
    def get(self, request):
        # Define the title for the news dashboard
        title = "News"

        # Make a GET request to the news API to retrieve the news articles
        news_articles = requests.get(
                            url = f"{HOSTNAME}/api/news/get_details/",
                            data = {}
                        ) 

        # Convert the JSON response into a Python dictionary
        response_data = json.loads(json.loads(news_articles.content).get('article_data:'))

        # Retrieve the top three articles from the response data
        top_three_articles = response_data[:3]

        # Retrieve the remaining articles from the response data
        remaining_articles = response_data[3:]

        # Render the news dashboard template and pass the relevant variables
        return render(request,'News/news_article_dashboard.html',locals())

class EditNewsArticle(View):
    def get(self, request, article_id):
        # Define the title for the page
        title = "Edit News"

        # Check if an article ID is provided in the URL
        if article_id:
            # Make a GET request to retrieve the news article with the specified ID
            url = f"{HOSTNAME}/api/news/get_details/?article_id={article_id}"
            news_article = requests.get(url=url)

            # Convert the JSON response into a Python dictionary
            article_content = json.loads(news_article.content)
            article = json.loads(article_content[0])
        
        # Render the edit news article page and pass the relevant variables
        return render(request,'News/edit_article.html',locals())
      
    def post(self, request, article_id):
        # Retrieve the POST data from the request
        self.post_data = request.POST

        # Store the article details in a dictionary
        article_details = {}
        article_details['news_article_id'] = self.post_data.get('id', '')
        article_details['name'] = self.post_data.get("article-name", '')
        article_details['description'] = self.post_data.get("article-description", '')
        article_details['author'] = self.post_data.get("article-author", '')
        article_details['source'] = self.post_data.get("source", '')

        # Check if any files were uploaded with the request
        if request.FILES:
            # Retrieve the attachment file from the request
            attachment = request.FILES.get('attachment')

            # Generate a unique folder name for the attachment
            folder_name = generate_hash()

            # Create a folder to store the attachment
            attachment_folder_path = os.path.join(ATTACHMENTS_PATH, folder_name)

            try:
                # Set the umask to 0 to ensure the folder has the correct permissions
                original_umask = os.umask(0)

                # Create the folder
                os.makedirs(attachment_folder_path)
            except Exception as e:
                # Redirect to the current page if there was an error creating the folder
                return redirect(request.path)
            finally:
                # Restore the original umask
                os.umask(original_umask)
            
            # Save the attachment to the folder
            attachment_folder_path = os.path.join(attachment_folder_path, attachment.name)

            try:
                with open(attachment_folder_path, 'wb+') as f:
                    for chunk in attachment.chunks():
                        f.write(chunk) 

                # Store the path to the attachment in the article details
                article_details['image_path'] = os.path.join("images",folder_name, str(attachment.name))
            except Exception as e:
                # Delete the attachment and redirect to the current page if there was an error saving the file
                os.remove(attachment_folder_path)
                return redirect(request.path)
        
        # Make a POST request to update the news article with the new details
        news_articles_api_resp = requests.post(
                            url = f"{HOSTNAME}/api/news/update/",
                            data = article_details,
                        )  

        # Check if the request was successful
        if news_articles_api_resp.status_code <= 299 and news_articles_api_resp.status_code >= 200:
            # Redirect to the news dashboard page if the article was updated successfully
            return redirect(f"{HOSTNAME}/")
        else:
            # Redirect to the current page if there was an error updating the article
            return redirect(request.path)
   
class ViewNewsArticle(View):
    def get(self, request,article_id):
        title = "View News"

        # check if article_id exists
        if article_id:
            # fetch the details of the news article using article_id
            url = f"{HOSTNAME}/api/news/get_details/?article_id={article_id}"
            news_article = requests.get(url=url)
            article_content = json.loads(news_article.content)
            article = json.loads(article_content[0])
        
        # render the view_news_article.html template with the news article details
        return render(request,'News/view_news_article.html',locals())
      
class CreateNewsArticle(View):
    def get(self, request):
        title = "Create News article"
        # render the create_article.html template for GET requests
        return render(request,'News/create_article.html',locals())

    def post(self, request):
        self.post_data = request.POST
        
        # retrieve article details from the POST request
        article_details = {}
        article_details['name'] = self.post_data.get("article-name",'')
        article_details['description'] = self.post_data.get("article-description",'')
        article_details['author'] = self.post_data.get("article-author",'')
        article_details['source'] = self.post_data.get("source",'')

        # if there are files in the request, save the attachment and update article details with image path
        if request.FILES:
            attachment = request.FILES.get('attachment')

            folder_name = generate_hash()
            attachment_folder_path = os.path.join(ATTACHMENTS_PATH, folder_name)
            print("attachments folder path:",attachment_folder_path)
            try:
                original_umask = os.umask(0)
                os.makedirs(attachment_folder_path)
            except Exception as e:
                print("exception:",e)
                return redirect(request.path)
            finally:
                os.umask(original_umask)
            
            attachment_folder_path = os.path.join(attachment_folder_path,attachment.name)
            print("attachment_folder_path:",attachment_folder_path)
            try:
                with open(attachment_folder_path, 'wb+') as f:
                    for chunk in attachment.chunks():
                        f.write(chunk) 

                article_details['image_path'] = os.path.join("images",folder_name,str(attachment.name))               
            except Exception as e:
                # if there's an error saving the attachment, delete the folder and redirect to same page
                os.remove(attachment_folder_path)
                return redirect(request.path)
        
        # make a POST request to the API to create the news article
        news_articles_api_resp = requests.post(
                            url = f"{HOSTNAME}/api/news/create/",
                            data = article_details,
                        )  
        if news_articles_api_resp.status_code <= 299 and news_articles_api_resp.status_code >= 200:
            # if the article was created successfully, redirect to news dashboard page
            return redirect(f"{HOSTNAME}/")
        else:
            # if there was an error creating the article, redirect to the same page
            return redirect(request.path)



def generate_hash():
    # Get the current date and time in the specified format
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Generate a random salt string of 10 characters
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Concatenate the current date/time and salt to form a unique string
    unique_str = now + salt

    # Hash the unique string using SHA256 and convert to hexadecimal format
    unique_hash = hashlib.sha256(unique_str.encode('utf-8')).hexdigest()

    # Return the first 25 characters of the hexadecimal hash
    return unique_hash[:25]
