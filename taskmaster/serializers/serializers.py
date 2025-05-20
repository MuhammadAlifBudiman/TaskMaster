from rest_framework import serializers
from ..models import *


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer validates the fields 'daily', 'weekly', 'monthly', 'execution_day', 'execution_time', and 'execution_date'.
    It ensures that only one of 'daily', 'weekly', or 'monthly' is selected and validates the presence and correctness of other fields based on the selected type.
    """

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        """
        Validate the data for the Task serializer.

        Args:
            data (dict): The data to be validated.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If any validation fails.
        """

        # Extract task type flags from the input data
        # Indicates if the task is a daily task
        daily = data.get('daily', False)
        # Indicates if the task is a weekly task
        weekly = data.get('weekly', False)
        # Indicates if the task is a monthly task
        monthly = data.get('monthly', False)

        # Extract execution-related fields from the input data
        # Day of the week for weekly tasks
        execution_day = data.get('execution_day')
        # Time of execution for all tasks
        execution_time = data.get('execution_time')
        # Date of execution for monthly tasks
        execution_date = data.get('execution_date')

        # Ensure only one of daily, weekly, or monthly is True
        # Count the number of task types selected
        options_count = sum([daily, weekly, monthly])
        if options_count != 1:
            raise serializers.ValidationError(
                {"type error": "Please select one and only one of 'Daily', 'Weekly', or 'Monthly'."}
            )

        # Ensure execution_time is provided for all tasks
        if not execution_time:
            raise serializers.ValidationError(
                {'execution_time': 'This field may not be blank.'})

        # Validate weekly tasks: execution_day must be provided
        if weekly and not execution_day:
            raise serializers.ValidationError(
                {'execution_day': 'This field may not be blank.'})

        # Validate monthly tasks: execution_date must be provided
        if monthly and not execution_date:
            raise serializers.ValidationError(
                {'execution_date': 'This field may not be blank.'})

        # Check if the execution_day is valid for weekly tasks
        valid_days = ["Sunday", "Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday", "Saturday"]  # Valid days of the week
        if execution_day and execution_day not in valid_days:
            raise serializers.ValidationError(
                {'execution_day': 'Invalid value. Choose from: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.'}
            )

        # Ensure no invalid fields are provided for daily tasks
        if daily and (execution_day or execution_date):
            raise serializers.ValidationError(
                {'dailytask': 'Invalid field for daily task.'})

        # Ensure no invalid fields are provided for weekly tasks
        if weekly and execution_date:
            raise serializers.ValidationError(
                {'weeklytask': 'Invalid field for weekly task.'})

        # Ensure no invalid fields are provided for monthly tasks
        if monthly and execution_day:
            raise serializers.ValidationError(
                {'monthlytask': 'Invalid field for monthly task.'})

        return data
