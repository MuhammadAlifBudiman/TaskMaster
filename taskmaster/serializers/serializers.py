from rest_framework import serializers
from ..models import *

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Provides validation for the 'daily', 'weekly', 'monthly', 'execution_day', 'execution_time', and 'execution_date' fields.

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

        daily = data.get('daily', False)
        weekly = data.get('weekly', False)
        monthly = data.get('monthly', False)
        execution_day = data.get('execution_day')
        execution_time = data.get('execution_time')
        execution_date = data.get('execution_date')

        # Ensure only one of daily, weekly, or monthly is True
        options_count = sum([daily, weekly, monthly])
        if options_count != 1:
            raise serializers.ValidationError(
                {"type error": "Please select one and only one of 'Daily', 'Weekly', or 'Monthly'."}
            )

        if not execution_time:
            raise serializers.ValidationError({'execution_time': 'This field may not be blank.'})

        if weekly and not execution_day:
            raise serializers.ValidationError({'execution_day': 'This field may not be blank.'})

        if monthly and not execution_date:
            raise serializers.ValidationError({'execution_date': 'This field may not be blank.'})

        # Check if the execution_day is valid
        valid_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if execution_day and execution_day not in valid_days:
            raise serializers.ValidationError(
                {'execution_day': 'Invalid value. Choose from: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.'}
            )

        # Ensure valid field for daily task
        if daily and (execution_day or execution_date):
            raise serializers.ValidationError({'dailytask': 'Invalid field for daily task.'})

        # Ensure valid field for weekly task
        if weekly and execution_date:
            raise serializers.ValidationError({'weeklytask': 'Invalid field for weekly task.'})

        # Ensure valid field for monthly task
        if monthly and execution_day:
            raise serializers.ValidationError({'monthlytask': 'Invalid field for monthly task.'})

        return data
