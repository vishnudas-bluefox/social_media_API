# Social_media_API
A general purpose social media API for all kind of social media developments

Build with :
* Python
* Django
* RestFramework

Database:
* postgresql

## API Endpoints
____________________
For localhost

### POST api/register/ for register the new user
```
http://localhost:8000/api/register/
```
The users credential will added to the user table
### POST /api/authenticate for validating the user and return jwt token as cookie for the further use
```
http://localhost:8000/api/authenticate/
```
The rest_framwork will authenticate the user and create a jwt token as cookie
### POST /api/follow/ for follow the user
```
http://localhost:8000/api/follow/
```
Users can follow any user the by simple passing the id. The logged user id will retrived from cookies
users get response when they follow same person multiple times

### POST /api/unfollow/ for unfollow the user
```
http://localhost:8000/api/follow/
```
Users can unfollow any user by passing the user id. The logged user id will rerive from cookie
users get response when they try to unfollow non followed user

### GET /api/user retrive the user profile detail with no_followers and no_following
```
http://localhost:8000/api/user/
```
The user id will retrive from the cookies. The user details such as no_followers and following will also return back

### POST api/posts/ create new post by validating the user 
```
http://localhost:8000/api/post/
```
### POST api/like/ to like the posts
```
http://localhost:8000/api/like/
```
