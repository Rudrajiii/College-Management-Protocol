let examList = [];
let count = 1;
let editingExamId = null;
let isDarkMode = true;

function openModal() {
    document.getElementById('addExamModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('addExamModal').style.display = 'none';
    resetForm();
}

function addExam() {
    const examName = document.getElementById('examName').value;
    const studentYear = document.getElementById('studentYear').value;
    const studentBranch = document.getElementById('studentBranch').value;
    const subject = document.getElementById('subject').value;
    const examDate = document.getElementById('examDate').value;
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;

    if (!Number.isInteger(+studentYear) || +studentYear <= 0) {
        alert('Student Year must be a positive integer!');
        return;
    }

    if (examName && studentYear && studentBranch && subject && examDate && startTime && endTime) {
        const examDetails = {
            id: count,
            examName,
            studentYear,
            studentBranch,
            subject,
            examDate,
            startTime,
            endTime
        };

        examList.push(examDetails);
        renderTable();
        count++;
        resetForm();
        closeModal();
    } else {
        alert('Please fill in all the fields!');
    }
}

function renderTable() {
    const tableBody = document.getElementById('examTableBody');
    tableBody.innerHTML = '';

    examList.forEach((exam) => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${exam.examName}</td>
            <td>${exam.studentYear}</td>
            <td>${exam.studentBranch}</td>
            <td>${exam.subject}</td>
            <td>${exam.examDate}</td>
            <td>${exam.startTime} - ${exam.endTime}</td>
            <td><button onclick="editExam(${exam.id})">Edit</button></td>
            <td><button onclick="deleteExam(${exam.id})">Delete</button></td>
        `;

        tableBody.appendChild(row);
    });
}

function editExam(id) {
    const exam = examList.find(exam => exam.id === id);
    if (exam) {
        document.getElementById('examName').value = exam.examName;
        document.getElementById('studentYear').value = exam.studentYear;
        document.getElementById('studentBranch').value = exam.studentBranch;
        document.getElementById('subject').value = exam.subject;
        document.getElementById('examDate').value = exam.examDate;
        document.getElementById('startTime').value = exam.startTime;
        document.getElementById('endTime').value = exam.endTime;

        editingExamId = id;
        document.getElementById('formActionBtn').textContent = 'Save Exam';
        openModal();
    }
}

function deleteExam(id) {
    examList = examList.filter(exam => exam.id !== id);
    renderTable();
}

function resetForm() {
    document.getElementById('examForm').reset();
    document.getElementById('formActionBtn').textContent = 'Add Exam';
    editingExamId = null;
}

function toggleTheme() {
    const root = document.documentElement;
    isDarkMode = !isDarkMode;

    if (isDarkMode) {
        root.style.setProperty('--background-color', 'black');
        root.style.setProperty('--text-color', 'white');
        root.style.setProperty('--button-bg-color', 'grey');
    } else {
        root.style.setProperty('--background-color', 'white');
        root.style.setProperty('--text-color', 'black');
        root.style.setProperty('--button-bg-color', 'grey');
    }
}
