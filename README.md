# Delivery App
Simple app made with Kivy for registering deliveries for. This was a freelance project, to help a friend who delivered food.

## Some things I learned in this project:

- Kivy - Kivy is a cross-platform framework for writing desktop and mobile apps. 
- KivyMD - Matherial Design widgets for Kivy.
- Buildozer - The app can be compiled do run on Android phone.
- Oauth protocol - This app uses Google Oauth, so you can log in with your Google account.
- Google Firebase - The app uses the Google Firebase Real Time Database to store data (json).

## Instalation:
#### Some sensitive data was removed from source, but some of them must be hardcoded when compiling for android.
#### This code will not run if you run in without editing the `main.py` and `classes/firebase_manager.py` files.


### For desktop (only tested Linux):
```sh
git clone https://github.com/arthur-bryan/delivery-app
cd delivery-app
python3 -m pip install -r requirements.txt
python3 main.py
```

### For Android:
- Do the same step as above, but don run the main.py yet.
- Install the compilation auxiliar [buildozer]("https://buildozer.readthedocs.io/en/latest/installation.html")
- Edit the `buildozer.spec` file to meet the requeriments for compiling for your Android.
- Run:
    ```sh
    buildozer android debug deploy run
    ```
  
#### PS: Your phone must be with USB debugging enabled and the USB cable connected to the PC. First compile should take more than 5 minutes.
- Search about hot to complie the binary and sign it (this is needed for the OAuth to work).

![login-app](https://user-images.githubusercontent.com/34891953/180631047-7b2bb5cc-4502-42c7-ba44-60dee7fef3eb.png)
![main-app](https://user-images.githubusercontent.com/34891953/180631048-a6e251d5-da26-468b-a9af-dc768a9eb92e.png)
![main-app-2](https://user-images.githubusercontent.com/34891953/180631049-2ec2496c-f4fa-4175-8a82-8688119cb308.png)
![main-app-3](https://user-images.githubusercontent.com/34891953/180631050-13d616df-13a0-4c9d-9ae6-6822c3fa907c.png)
![main-app-4](https://user-images.githubusercontent.com/34891953/180631051-8cb4405d-9901-4390-b7cc-fc1bc1c4b519.png)
![main-app-db-update](https://user-images.githubusercontent.com/34891953/180631052-176fdfe9-443c-4a79-a88f-a6abff9e198e.png)
![new-stablishment-app](https://user-images.githubusercontent.com/34891953/180631053-b844b491-4f85-41f9-8c7f-e146ef32787a.png)
![image](https://user-images.githubusercontent.com/34891953/180631064-74b851a2-37bd-4600-9073-dac5c2d08d1a.png)
![image](https://user-images.githubusercontent.com/34891953/180631074-e2814a8e-81b6-4347-878a-1f3f18a32078.png)
![image](https://user-images.githubusercontent.com/34891953/180631085-ec5dcbd2-286b-4ce7-a3db-125c5825a532.png)