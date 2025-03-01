# creating a visual environment for the user to interact with the program
# installing the necessary libraries pandas, openpyxl ,mysql-connector-python, matplotlib ,plotly 
# importing pandas library
import streamlit as st
import pandas as pd
from backend import database

def exportDoctors():
    doctors_df = database.read_doctors()
    doctors_df.to_excel("doctors.xlsx", index=False)

def exportNurses():   
    nurses_df = database.read_nurses()
    nurses_df.to_excel("nurses.xlsx", index=False)

def exportAppointments():
    appointments_df = database.read_appointments()
    appointments_df.to_excel("appointments.xlsx", index=False)

def exportPatients():
    patients_df = database.read_patients()
    patients_df.to_excel("patients.xlsx", index=False)









# Perform Statistical Analysis 
import matplotlib.pyplot as plt
import plotly.express as px



def patientByDoctor():
    patientsbyDoctor = database.patient_by_doctor()
    print(patientsbyDoctor)
    plt.figure(figsize=(8, 5))
    patientsbyDoctor.plot(x="doctor_name", y="patient_count", kind="bar", color="skyblue", legend=False)
    plt.xlabel("Doctor")
    plt.ylabel("Number of Patients")
    plt.title("Patients by Doctor")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(plt)

def appointmentStatu():
    fig = px.pie(
        database.read_appointments(), 
        names="status", 
        title="Appointment Status Distribution", 
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)



def patientAge():
    plt.figure(figsize=(8,5))
    plt.hist(database.read_patients()["age"], bins=5, color="lightcoral", edgecolor="black", alpha=0.7)
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.title("Patient Age Distribution")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(plt)
 

















