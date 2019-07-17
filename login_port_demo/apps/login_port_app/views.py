from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "login_port_app/index.html")

def process_reg(request):
    print("Hit process_reg route")

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.registration_validator(request.POST)

    # IF we have errors
    if len(errors) > 0:
        # loop through each key-value pair IN ERRORS and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # kick them from whence them came
        print("Registration validation failed! Kicking out to index")
        return redirect('/')
    # ELSE we dont have errors
    else:
        # Lets register the new user!
        hashed_password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        print(f"****************************** hash_password = {hashed_password}")
        created_user = User.objects.create(email=request.POST["email"], password=hashed_password)
        print(f"Successfully registered!!!!! created_user = {created_user}")

        # Log in user
        request.session["logged_in_user_id"] = created_user.id

        return redirect('/dashboard')

def process_log(request):
    print("Hit process_log route")

    # Try to run this code, if there are no errors, no problem!
    try:
        logging_in_user = User.objects.get(email=request.POST['email'])
        # Run query on user
        if bcrypt.checkpw(request.POST['password'].encode(), logging_in_user.password.encode()):
            print("password match successful!")

            # Log in user
            request.session["logged_in_user_id"] = logging_in_user.id
            return redirect('/dashboard')
        else:
            print("failed password")
            # Add validation error and kick them out to the index
            messages.error(request, "Login credentials do not match the database")
            return redirect("/")
    # If you hit an error, instead of breaking, run this code
    except:
        # Add validation error and kick them out to the index
        messages.error(request, "Login credentials do not match the database")
        return redirect("/")



    return redirect('/dashboard')

def dashboard(request):
    # If the user is not logged in, kick them to loginreg
    if 'logged_in_user_id' not in request.session:
        return redirect("/")
    return render(request, "login_port_app/dashboard.html")

def logout(request):
    request.session.clear()
    return redirect("/")