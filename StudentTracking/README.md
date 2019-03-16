It is a web based student tracking system.This is a training program for certain age ranges.
In the training process,assignments are given according to the success of the students and reports are prepared by the instructor.

Framework ->Django

Database ->MySQL

-------------------Environment------------------------------------------

Python Packages:

Django(2.1.5)

django-bootstrap-datepicker-plus(3.0.5)

django-crispy-form (1.7.2)

django-extra-views (0.12.0)

mysqlclient (1.3.14)

pip	(10.0.1)

pytz(2018.9)

setuptools	(39.1.0)

six	(1.12.0)

-----------------------Stored Procedure----------------------------------

Stored Procedure = StudentCounybyID

--------------------Code-------------------------------------------------

 cursor = connection.cursor()
    try:
        cursor.callproc('StudentCountbyID')
        studentcounts = cursor.fetchall()

    finally:
        cursor.close()

--------------------------Transaction-------------------------------------

    def form_valid(self, form): 
        obj = form.save(commit=False)
        obj.userID = Teacher.objects.get(user_id=self.request.user)
        obj.save()
        return super().form_valid(form)
