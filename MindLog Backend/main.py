from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .database import Base, engine, get_db
from .models import Usuario, Registro
from .utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MindLog API")

# Configurar CORS para que el frontend pueda hacer peticiones
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://mindproject.netlify.app",
    # Añade más dominios según despliegues frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para registro de usuarios
@app.post("/register", status_code=201)
def register_user(user: Usuario, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user.password = hash_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "Usuario registrado correctamente"}

# Ruta para login y obtención del token JWT
@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para crear un registro de emociones nuevo (diario)
@app.post("/registros")
def create_registro(
    texto: str,
    emociones: list[str],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    nuevo_registro = Registro(
        texto=texto,
        emociones=",".join(emociones),
        usuario_id=current_user.id
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

# Ruta para obtener todos los registros del usuario
@app.get("/registros")
def get_registros(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    registros = db.query(Registro).filter(Registro.usuario_id == current_user.id).all()
    return registros

# Ruta para borrar un registro por id
@app.delete("/registros/{registro_id}", status_code=204)
def delete_registro(
    registro_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    registro = db.query(Registro).filter(
        Registro.id == registro_id,
        Registro.usuario_id == current_user.id
    ).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(registro)
    db.commit()
    return

# Ruta para obtener información básica del usuario actual
@app.get("/me")
def read_current_user(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

# Ruta para saludos o prueba rápida
@app.get("/")
def root():
    return {"msg": "MindLog API funcionando correctamente."}
