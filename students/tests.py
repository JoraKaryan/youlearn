from django.test import TestCase

# Create your tests here.

# in_students_list.html
'''
                    <td>
                        <a href="{% url 'student_detail' student.id %}" class="btn btn-info btn-sm">View</a>
                        <a href="{% url 'student_edit' student.id %}" class="btn btn-warning btn-sm">Edit</a>
                        <a href="{% url 'student_delete' student.id %}" class="btn btn-danger btn-sm" 
   onclick="return confirm('Are you sure you want to delete this student?');">
   Delete
</a>

                    </td>
'''