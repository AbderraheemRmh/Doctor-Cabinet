import streamlit as st
from streamlit_option_menu import option_menu
from backend import database
from export import export
from importdata import importdata


def show():
    # Initialize session state for doctors, nurses, patients, and appointments
    if "doctors" not in st.session_state:
        st.session_state.doctors = []

    if "nurses" not in st.session_state:
        st.session_state.nurses = []

    if "patients" not in st.session_state:
        st.session_state.patients = []

    if "appointments" not in st.session_state:
        st.session_state.appointments = []

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Dashboard",
            options=["Doctors", "Nurses", "Patients", "Appointments", "Statistics"],
            icons=["doctor", "nurse", "person", "calendar", "chart-bar"],
            menu_icon="cast",
            default_index=0
        ) 
    if st.button("Import Data"):
        importdata.importData()
    # Doctors Section
    if selected == "Doctors":
        doctor_option = st.sidebar.selectbox("Manage Doctors", ["Add Doctor", "Show Doctors"])
        st.title(f"{selected} Page")

        if doctor_option == "Add Doctor":
            st.subheader("➕ Add a Doctor")
            username = st.text_input("Username")
            password = st.text_input("Password")
            name = st.text_input("Name")
            specialty = st.text_input("Specialty")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            if st.button("Add Doctor"):
                if username and password and name and specialty and phone and email:
                    database.create_doctor(username, password, name, specialty, phone, email)
                    st.success("Doctor created")
                    st.rerun()
                else:
                    st.error("All fields must be filled")

        elif doctor_option == "Show Doctors":
            st.subheader("📋 List of Doctors")
            doctorsDF = database.read_doctors()
            doctorsDF["Delete"] = [False] * len(doctorsDF)
            edited_df = st.data_editor(
                doctorsDF,
                column_config={
                    "Delete": st.column_config.CheckboxColumn("Delete"),
                },
                key="appointments_table"
            )
            if st.button("Delete Doctor"):
                for i in range(len(edited_df)):
                    if edited_df.loc[i, "Delete"]:  # If checkbox is checked
                        appointment_id = str(edited_df.loc[i, "id"])
                        database.delete_doctor(appointment_id)
            if st.button("Export to excel"):
                export.exportDoctors()

    # Nurses Section
    if selected == "Nurses":
        nurse_option = st.sidebar.selectbox("Manage Nurses", ["Add Nurse", "Show Nurses"])
        st.title(f"{selected} Page")

        if nurse_option == "Add Nurse":
            st.subheader("➕ Add a Nurse")
            username = st.text_input("Username")
            password = st.text_input("Password")
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            if st.button("Add Nurse"):
                if username and password and name and phone and email:
                    database.create_nurse(username, password, name, phone, email)
                    st.success("Nurse created")
                    st.rerun()
                else:
                    st.error("All fields must be filled")


        elif nurse_option == "Show Nurses":
            st.subheader("👩‍⚕️ List of Nurses")
            nursesDF = database.read_nurses()
            nursesDF["Delete"] = [False] * len(nursesDF)
            edited_df = st.data_editor(
                nursesDF,
                column_config={
                    "Delete": st.column_config.CheckboxColumn("Delete"),
                },
                key="appointments_table"
            )
            if st.button("Delete Nurse"):
                for i in range(len(edited_df)):
                    if edited_df.loc[i, "Delete"]:  # If checkbox is checked
                        appointment_id = str(edited_df.loc[i, "id"])
                        database.delete_nurse(appointment_id)
            if st.button("Export to excel"):
                export.exportNurses()


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
            patientDF["Delete"] = [False] * len(patientDF)
            edited_df = st.data_editor(
                patientDF,
                column_config={
                    "Delete": st.column_config.CheckboxColumn("Delete"),
                },
                key="appointments_table"
            )
            if st.button("Delete Patients"):
                for i in range(len(edited_df)):
                    if edited_df.loc[i, "Delete"]:  # If checkbox is checked
                        appointment_id = str(edited_df.loc[i, "id"])
                        database.delete_patient(appointment_id)
            if st.button("Export to excel"):
                export.exportPatients()


        
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
            
            # Add a checkbox column
            appointmentDF["Mark as Done"] = [False] * len(appointmentDF)
            appointmentDF["Mark as Cancelled"] = [False] * len(appointmentDF)

            # Display editable DataFrame
            edited_df = st.data_editor(
                appointmentDF,
                column_config={
                    "Mark as Done": st.column_config.CheckboxColumn("Done"),
                    "Mark as Cancelled": st.column_config.CheckboxColumn("Cancelled")
                },
                key="appointments_table"
            )

            # Button to update selected rows
            if st.button("Update Appointments"):
                for i in range(len(edited_df)):
                    appointment_id = str(edited_df.loc[i, "id"])
                    if edited_df.loc[i, "Mark as Done"]:  # If checkbox is checked
                        database.update_appointment_status(appointment_id, "done")
                    elif edited_df.loc[i, "Mark as Cancelled"]:  
                        database.update_appointment_status(appointment_id, "canceled")  # Update to "Cancelled"
            if st.button("Export to excel"):
                export.exportAppointments()




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



