import streamlit as st
from streamlit_option_menu  import option_menu
from backend import database
from export import export
def show():
    if "patient" not in st.session_state:
        st.session_state.patients = []
    if "appointments" not in st.session_state: 
        st.session_state.appointments = []
    if "statics" not in st.session_state:
        st.session_state.statics = []        
    #side bar menu
    with st.sidebar :
        selected = option_menu(
            menu_title="Nursing",
            options = [  "Patients" , "Appointments" , "Statistics"],
            icons = ["person","calendar","bar charts"],
            menu_icon = "cast",
            default_index=0

        )

    if selected == "Patients":
        patient_option = st.sidebar.selectbox("Manage Patients", ["Add Patient", "Show Patients"])
        st.title(f"{selected} Page")

        if patient_option == "Add Patient":
            st.subheader("➕ Add a Patient")
            name = st.text_input("Name")
            age = st.text_input("Age")
            gender = st.radio("Gender" , ["Male" , "Female"])
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            illness = st.text_area ("Illness or describe it")
            if st.button("Add Patient"):
                if name and age and gender and phone and illness:
                    database.create_patient(name, age, "M" if gender == "Male" else "F", phone, email, illness)
                    st.success("Patient added")
                    st.rerun()
                else:
                    st.error("All fields must be filled")


        elif patient_option == "Show Patients":
            st.subheader("📋 List of Patients")
            patientDF = database.read_patients()
            st.dataframe(patientDF)


        
    if selected == "Appointments":
        appointment_option = st.sidebar.selectbox("Manage Appointments", ["All Appointments", "Add an Appointment"])
        st.title(f"{selected} Page")

        if appointment_option == "Add an Appointment":
            st.subheader("📅 Schedule an Appointment")

            patient = st.selectbox("Select Patient", database.read_patients()["name"])
            nurse = st.selectbox("Select Nurse", database.read_nurses()["name"])
            doctor = st.selectbox("Select Doctor", database.read_doctors()["name"])
            date = st.date_input("Select Date")
            time = st.time_input("Select Time")

            if st.button("Add Appointment"):
                if patient and nurse and doctor and date and time:
                    database.create_appointment(database.read_patient_id(patient), database.read_nurse_id(nurse), database.read_doctor_id(doctor), date, time, "pending")
                    st.success("Appointment added")
                    st.rerun()
                else:
                    st.error("All fields must be filled")

        elif appointment_option == "All Appointments":
            st.subheader("📋 Appointment List")
            appointmentDF = database.read_appointments()
            st.dataframe(appointmentDF)




    # Statistics Section
    if selected == "Statistics":
        st.title("📊 Statistics")
        st.write("🔹 Total Doctors: ", len(database.read_doctors()))
        st.write("🔹 Total Nurses" , len(database.read_nurses()))
        st.write("🔹 Total Appointments" , len(database.read_appointments()))
        completed_appointments = list(filter(lambda x : x == "done",database.read_appointments()["status"]))
        st.write(f"✅ **Completed Appointments:** {len(completed_appointments)}")
        export.patientByDoctor()
        export.appointmentStatu()
        export.patientAge()
    

