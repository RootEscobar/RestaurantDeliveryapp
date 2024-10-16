from restaurant.routes import app

#Comprueba si main.py se ha ejecutado directamente y no se ha importado.
if __name__ == '__main__':
    app.run(debug = True)



