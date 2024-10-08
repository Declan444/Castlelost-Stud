### Automated Testing
 **Instructor Model Test** 
| **Test Name**         | **Description**                                                | **Assertion/Result**          |
|-----------------------|----------------------------------------------------------------|-------------------------------|
| test_instructor_creation | Verifies that an `Instructor` object can be created with valid data. | Passed - Instructor was created successfully |
| test_instructor_str_method | Ensures the `__str__()` method of the `Instructor` model returns the correct string. | Passed - Correct string representation |
| test_instructor_unique_slug | Confirms that two `Instructor` objects cannot share the same slug (ensures uniqueness). | Passed - Slug uniqueness enforced |

 **Lesson Model Test**
| **Test Name**         | **Description**                                               | **Assertion/Result**          |
|-----------------------|---------------------------------------------------------------|-------------------------------|
| test_lesson_creation | Check if the `lesson` was created correctly                    | Passed: Lesson instance created correctly |
| test_str_method      | Check the `string representation` of the Lesson instance       | Passed: String representation is correct |