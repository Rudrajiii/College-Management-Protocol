let examList = [];
let idCounter = 1;
let mainDetailsSet = false;
let editExamId = null;

// Set Main Exam Details
function setMainDetails() {
    const examName = document.getElementById('examName').value;
    const studentYear = document.getElementById('studentYear').value;
    const studentBranch = document.getElementById('studentBranch').value;

    if (examName && studentYear && studentBranch) {
        document.getElementById('examTitle').innerText = 
            `Exam Name: ${examName} | Year: ${studentYear} | Branch: ${studentBranch}`;
        document.getElementById('examHeader').style.display = 'block';
        mainDetailsSet = true;

        document.getElementById('examName').disabled = false;
        document.getElementById('studentYear').disabled = false;
        document.getElementById('studentBranch').disabled = false;
    } else {
        alert('Please enter Exam Name, Student Year, and Branch.');
    }
}

// Open Modal for Adding Data
function openModal() {
    if (!mainDetailsSet) {
        alert('Set Exam Name, Student Year, and Branch first!');
        return;
    }
    editExamId = null;
    document.getElementById('modalTitle').innerText = 'Add Exam Details';
    document.getElementById('modalForm').reset();
    document.getElementById('modal').style.display = 'flex';
}

// Close Modal
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Submit Data (Add or Edit)
function submitData() {
    const subject = document.getElementById('modalSubject').value;
    const examDate = document.getElementById('modalExamDate').value;
    const startTime = document.getElementById('modalStartTime').value;
    const endTime = document.getElementById('modalEndTime').value;

    if (subject && examDate && startTime && endTime) {
        const examTime = `${startTime} - ${endTime}`;

        if (editExamId !== null) {
            // Edit existing exam
            const index = examList.findIndex(exam => exam.id === editExamId);
            examList[index] = { id: editExamId, subject, examDate, time: examTime };
            editExamId = null;
        } else {
            // Add new exam
            const newExam = {
                id: idCounter++,
                subject,
                examDate,
                time: examTime
            };
            examList.push(newExam);
        }

        renderTable();
        closeModal();
    } else {
        alert('Please fill in all fields!');
    }
}

// Render Table
// Render Table
function renderTable() {
    const tableBody = document.getElementById('examTableBody');
    tableBody.innerHTML = '';

    examList.forEach((exam) => {
        const row = `
            <tr>
                <td>${exam.subject}</td>
                <td>${exam.examDate}</td>
                <td>${exam.time}</td>
                <td>
                    <button class="action-btn edit-btn" onclick="editExam(${exam.id})">Edit</button>
                    <button class="action-btn delete-btn" onclick="deleteExam(${exam.id})">Delete</button>
                </td>
            </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}


// Edit Exam
function editExam(id) {
    const exam = examList.find(item => item.id === id);

    if (exam) {
        editExamId = id;
        document.getElementById('modalTitle').innerText = 'Edit Exam Details';
        document.getElementById('modalSubject').value = exam.subject;
        document.getElementById('modalExamDate').value = exam.examDate;
        document.getElementById('modalStartTime').value = exam.time.split(' - ')[0];
        document.getElementById('modalEndTime').value = exam.time.split(' - ')[1];
        document.getElementById('modal').style.display = 'flex';
    }
}

// Delete Exam
function deleteExam(id) {
    examList = examList.filter(exam => exam.id !== id);
    renderTable();
}

// Submit All Data
function submitAllData() {
    if (examList.length > 0) {
        alert('All data submitted successfully!');
        console.log('Exam Data:', examList);
    } else {
        alert('No data to submit!');
    }
}

// Toggle Dark/Light Mode
// Toggle Dark/Light Mode

// Toggle dark and light mode on checkbox change
document.getElementById('toggleMode').addEventListener('change', function () {
    document.body.classList.toggle('light-mode', this.checked);
});

//fetching the table content for passing to backend

document.getElementById('submitButton').addEventListener('click', () => {
    const exam_name = document.getElementById('examName').value; 
    const student_year = document.getElementById('studentYear').value; 
    const student_branch = document.getElementById('studentBranch').value;
    const table = document.getElementById('data-table');
    const rows = table.querySelectorAll('tbody tr');
    const tableData = Array.from(rows).map(row => {
        const cells = row.querySelectorAll('td');
        return {
            subject: cells[0].textContent.trim(),
            date: cells[1].textContent.trim(),
            time: cells[2].textContent.trim(),
        };
    });
    const exam_data = {"exam_name": exam_name , "student_year": student_year , "student_branch": student_branch , "schedule": tableData};

    // Send data to Flask backend
    fetch('/exam_scheduler', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: exam_data })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        // Redirect to the admin dashboard
        window.location.href = "/admin_dashboard";
    })
    .catch(error => console.error('Error:', error));
});




