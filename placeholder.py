def launch_experience(experience_id):
    startExperience(experience_id)
    Tail.tail()
    time.sleep(10)

def launch_selected_experiences():
    max_retries = 3  # Maximum number of retries
    retry_count = 0

    while retry_count < max_retries:
        try:
            experiences = read_experiences_from_spreadsheet()
            selected_experiences = [experience_name for experience_var, experience_name in zip(experience_vars, experiences) if experience_var.get() == 1]

            print("Selected experiences:", selected_experiences)

            for experience_name in selected_experiences:
                experience_id = experiences.get(experience_name)

                if experience_id:
                    print("Experience Name:", experience_name)
                    print("Experience ID:", experience_id)

                    launch_experience(experience_id)
                    check_and_kill_application()  # Check for application misbehavior
                    time.sleep(10)  # Sleep between experiences
        except Tail.Catch5:
            retry_count += 1
            print(f"Application misbehaving. Retrying ({retry_count}/{max_retries})...")
        else:
            break  # No exception occurred, break out of the loop
    else:
        print("Max retries reached. Could not launch experiences.")

# Call the function
launch_selected_experiences()
