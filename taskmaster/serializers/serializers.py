from rest_framework import serializers
import re
from ..models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__' 
 
    def validate(self, data):
        daily = data.get('daily', False)
        weekly = data.get('weekly', False)
        monthly = data.get('monthly', False)
        execution_day = data.get('execution_day')
        execution_time = data.get('execution_time')
        execution_date = data.get('execution_date')

        # Ensure only one of daily, weekly, or monthly is True
        options_count = sum([daily, weekly, monthly])
        if options_count != 1:
            raise serializers.ValidationError({"type error": "Please select one and only one of 'Daily', 'Weekly', or 'Monthly'."})

        if not execution_time:
            raise serializers.ValidationError({'execution_time': 'This field may not be blank.'})

        if weekly and not execution_day:
            raise serializers.ValidationError({'execution_day': 'This field may not be blank.'})

        if monthly and not execution_date:
            raise serializers.ValidationError({'execution_date': 'This field may not be blank.'})

        # Check if the execution_time is valid
        time_pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d):(\d\d)$')
        if execution_time and not time_pattern.match(str(execution_time)):
            raise serializers.ValidationError({'execution_time': 'Invalid time format. Use the format HH:mm.'})

        # Check if the execution_day is valid
        valid_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if execution_day and execution_day not in valid_days:
            raise serializers.ValidationError({'execution_day': 'Invalid value. Choose from: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.'})

        # Check if the execution_date day is in the range 1-31
        if execution_date and (execution_date < 1 or execution_date > 31):
            raise serializers.ValidationError({'execution_date': 'Invalid day. Choose a day between 1 and 31.'})


        if not daily and not weekly and not monthly:
            raise serializers.ValidationError({'type errors': 'choose from: daily, weekly, monthly'})

        # Ensure valid field for dailytask
        if daily and (execution_day or execution_date):
            raise serializers.ValidationError({'dailytask': 'Invalid field for daily task.'})

        # Ensure valid field for weekly task:
        if weekly and execution_date:
            raise serializers.ValidationError({'weeklytask': 'Invalid field for weekly task.'})

        # Ensure valid field for monthly task:
        if monthly and execution_day:
            raise serializers.ValidationError({'monthlytask': 'Invalid field for monthly task.'})



        return data






