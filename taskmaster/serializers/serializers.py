from rest_framework import serializers
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

        if not execution_time:
            raise serializers.ValidationError({'execution_time': 'This field may not be blank.'})

        if weekly and not execution_day:
            raise serializers.ValidationError({'execution_day': 'This field may not be blank.'})

        if monthly and not execution_date:
            raise serializers.ValidationError({'execution_date': 'This field may not be blank.'})

        # Check if the execution_day is valid
        valid_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if execution_day and execution_day not in valid_days:
            raise serializers.ValidationError({'execution_day': 'Invalid value. Choose from: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.'})

        # Check if the execution_date day is in the range 1-31
        if execution_date and (execution_date < 1 or execution_date.day > 31):
            raise serializers.ValidationError({'execution_date': 'Invalid day. Choose a day between 1 and 31.'})


        if not daily and not weekly and not monthly:
            raise serializers.ValidationError({'type errors': 'choose from: daily, weekly, monthly'})

        return data






