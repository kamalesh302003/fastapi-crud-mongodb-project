from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

app=FastAPI()

#MongoDB Connection
client=MongoClient("mongodb://localhost:27017")

#Database
db=client["studentdb"]

#Collection
collection=db["students"]

#Pydantic Model
class Student(BaseModel):
    name:str
    age:int
    email:str

#Home Route
@app.get("/home")
def home():
    return {"message":"FastAPI MongoDB Connection"}

#CREATE Student
@app.post("/students/")
def create_student(student:Student):

    data={
        "name":student.name,
        "age":student.age,
        "email":student.email
    }

    collection.insert_one(data)

    return {"message":"Student Added Successfully"}

#READ ALL Students
@app.get("/students/")
def get_students():
    students=[]
    for student in collection.find():
        students.append({
            "id":str(student["_id"]),
            "name":student["name"],
            "age":student["age"],
            "email":student["email"]
        })
    return students

#UPDATE Student
@app.put("/students/{student_id}")
def update_student(student_id:str,student: Student):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400,detail="Invalid student ID")

    updated=collection.update_one(
        {"_id":ObjectId(student_id)},
        {"$set":{"name":student.name,"age":student.age,"email":student.email}}
    )

    if updated.matched_count==0:
        raise HTTPException(status_code=404,detail="Student not found")

    return {"message":"Student Updated Successfully"}

#DELETE Student
@app.delete("/students/{student_id}")
def delete_student(student_id:str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400,detail="Invalid student ID")

    deleted=collection.delete_one({"_id":ObjectId(student_id)})
    if deleted.deleted_count==0:
        raise HTTPException(status_code=404,detail="Student not found")
    return {"message":"Student Deleted Successfully"}