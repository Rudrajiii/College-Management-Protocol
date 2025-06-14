let idCounter = 1;

// started 17/2 - left side data 

function openModal() {
   /**
 * The openModal function is responsible for displaying the modal to add exam details.
 * It first checks if the main exam details are set 
 * If not, it alerts the user to set the exam details first and exits the function.
 * When adding a new exam, the editExamId is reset to null.
 * The modal title is updated to "Add Exam Details," and the form within the modal is reset to clear any previous input.
 * Finally, the modal is displayed by setting its style to 'flex', allowing the user to input new exam details.
 */
    if (!mainDetailsSet) {
        alert('Set Exam details first!');
        return;
    }
    editExamId = null;
    document.getElementById('modalTitle').innerText = 'Add Exam Details';
    document.getElementById('modalForm').reset();
    document.getElementById('modal').style.display = 'flex';
}




function closeModal() {
    document.getElementById('modal').style.display = 'none';
}




function submitData() {
    /**
     * Validates form fields, checks unique code, formats date/time, updates or adds exam, and refreshes the table display.
     */
    const subject = document.getElementById('modalSubject').value.trim();
    const code = document.getElementById('modalSubjectCode').value.trim();
    const examDate = document.getElementById('modalExamDate').value.trim();
    const startTime = document.getElementById('modalStartTime').value.trim();
    const endTime = document.getElementById('modalEndTime').value.trim();

   
    if (!subject || !code || !examDate || !startTime || !endTime) {
        alert('Please fill in all fields!');
        return;
    }
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(examDate)) {
        alert('Invalid date format. Please use YYYY-MM-DD.');
        return;
    }
    const timeRegex = /^\d{2}:\d{2}$/;
    if (!timeRegex.test(startTime) || !timeRegex.test(endTime)) {
        alert('Invalid time format. Please use HH:MM.');
        return;
    }
    if (editExamId === null && examList.some(exam => exam.code === code)) {
        alert('Subject code already exists. Please use a unique code.');
        return;
    }

    const examTime = `${startTime} - ${endTime}`;

    if (editExamId !== null) {
        const index = examList.findIndex(exam => exam.id === editExamId);
        if (index !== -1) {
            examList[index] = { id: editExamId, subject, code, examDate, time: examTime };
        }
        editExamId = null; 
    } else {
        
        const newExam = {
            id: idCounter++,
            subject,
            code,
            examDate,
            time: examTime
        };
        examList.push(newExam);
    }
    renderTable();
    closeModal();
}





function renderTable() {
    /**
     * Displays exam list in a table by dynamically creating rows with subject, code, date, and time details.
     */
    const tableBody = document.getElementById('examTableBody'); 
    tableBody.innerHTML = ''; 

    examList.forEach(exam => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${exam.subject}</td>
            <td>${exam.code}</td> <!-- Ensure this matches the mapped field -->
            <td>${exam.examDate}</td>
            <td>${exam.time}</td>
        `;
        tableBody.appendChild(row);
    });
}





function editExam(id) {
    /**
     * helps to edit details after setig the details from right div**/
    const exam = examList.find(item => item.id === id);

    if (exam) {
        editExamId = id;
        document.getElementById('modalTitle').innerText = 'Edit Exam Details';
        document.getElementById('modalSubject').value = exam.subject;
        document.getElementById('modalSubjectCode').value = exam.code;
        document.getElementById('modalExamDate').value = exam.examDate;
        document.getElementById('modalStartTime').value = exam.time.split(' - ')[0];
        document.getElementById('modalEndTime').value = exam.time.split(' - ')[1];
        document.getElementById('modal').style.display = 'flex';
    }
}



function deleteExam(id) {
    /** delete the data */
    examList = examList.filter(exam => exam.id !== id);
    renderTable();
}

/**------------------------------------------------------------------------------------------------------------------------------------------------------------------------**/
// resumed on 18/2 Fetching the table content for passing to backend
document.getElementById('submitButton').addEventListener('click', () => {
    const exam_name = document.getElementById('examName').value; 
    const student_year = document.getElementById('studentYear').value; 
    const student_branch = document.getElementById('studentBranch').value;
    const student_venue = document.getElementById('studentvenue').value;
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
    const exam_data = {"exam_name": exam_name , "student_year": student_year , "student_branch": student_branch ,"student_venue ": student_venue  ,"schedule": tableData};

    // Send data to Flask backend and
    //  will redirect to admin dashboard
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
       
        window.location.href = "/admin_dashboard";
    })
    .catch(error => console.error('Error:', error));
});




function showSuccessPopup() {
    const popup = document.getElementById('successPopup');
    popup.style.display = 'block';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000); // 3 seconds
}
const quotes = [
    "The future depends on what you do today. – Mahatma Gandhi",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Do what you can, with what you have, where you are. – Theodore Roosevelt",
];




function displayRandomQuote() {
    //set new quotes 
    const quoteElement = document.getElementById('dynamicQuote');
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    quoteElement.innerText = randomQuote;
}





function previewSchedule() {
    /// Open Preview form
    if (examList.length === 0) {
        alert('No data to preview!');
        return;
    }

    const previewTableContainer = document.getElementById('previewTableContainer');
    previewTableContainer.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Subject</th>
                    <th>Subject code</th>
                    <th>Exam Date</th>
                    <th>Exam Time</th>
                </tr>
            </thead>
            <tbody>
                ${examList.map(exam => `
                    <tr>
                        <td>${exam.subject}</td>
                        <td>${exam.code}</td> 
                        <td>${exam.examDate}</td>
                        <td>${exam.time}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    document.getElementById('previewModal').style.display = 'flex';
    document.getElementById('submitButton').style.display = 'inline-block'; 
}




function closePreviewModal() {
    // Close Preview Modal
    document.getElementById('previewModal').style.display = 'none';
}




function printPreview() {
    window.print();
}
document.getElementById('submitButton').addEventListener('click', () => {
    // Collect input values and fetching the table content for passing to backend
    const exam_name = document.getElementById('examName').value.trim();
    const student_year = document.getElementById('studentYear').value.trim();
    const student_branch = document.getElementById('studentBranch').value.trim();
    const student_venue = document.getElementById('studentvenue').value.trim();
    if (!exam_name || !student_year || !student_branch || !student_venue) {
        alert('Please fill in all fields!');
        return;
    }

    const table = document.getElementById('data-table');
    const rows = table.querySelectorAll('tbody tr');
    const tableData = Array.from(rows).map(row => {
        const cells = row.querySelectorAll('td');
        return {
            subject: cells[0].textContent.trim(),
            code: cells[1].textContent.trim(), 
            date: cells[2].textContent.trim(),
            time: cells[3].textContent.trim(),
        };
    })
    if (tableData.length === 0) {
        alert('No exam schedule data found. Please add at least one exam.');
        return;
    }

    const exam_data = {
        exam_name: exam_name,
        student_year: student_year,
        student_branch: student_branch,
        student_venue: student_venue,
        schedule: tableData
    };

    // Send data to Flask backend
    fetch('/exam_scheduler', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: exam_data })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response from server:', data);
        alert('Exam data submitted successfully!');
        window.location.href = "/admin_dashboard"; // Redirect to admin dashboard
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to submit data. Please try again.');
    });
});





// Print Preview
function printPreview() {
    const examDetailsDisplay = document.getElementById('examDetailsDisplay').innerHTML;
    const printContent = `
        <h2>Exam Schedule</h2>
        <div id="printExamDetails">
            ${examDetailsDisplay}
        </div>
        <div id="printTableContainer">
            ${document.getElementById('previewTableContainer').innerHTML}
        </div>
        <div class="quote-container">
            <p id="dynamicQuote">${document.getElementById('dynamicQuote').innerText}</p>
        </div>
    `;

    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write(`
        <html>
            <head>
                <title>Exam Schedule</title>
                <style>
                    body { font-family: 'Montserrat', sans-serif; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
                    th { background-color: #7B1FA2; color: white; }
                    .quote-container { text-align: center; margin-top: 20px; font-style: italic; color: #555; }
                    #printExamDetails { margin-bottom: 20px; }
                    #printExamDetails p { margin: 5px 0; }
                </style>
            </head>
            <body>
                ${printContent}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}
let examList = [];
let mainDetailsSet = false;
let editExamId = null;
//  dropdown
document.getElementById('examName').addEventListener('change', function () {
    const customExamNameInput = document.getElementById('customExamName');
    if (this.value === 'Custom') {
        customExamNameInput.style.display = 'block';
    } else {
        customExamNameInput.style.display = 'none';
    }
});






function setMainDetails() {
    const examNameDropdown = document.getElementById('examName');
    const customExamNameInput = document.getElementById('customExamName');
    const examName = examNameDropdown.value === 'Custom' ? customExamNameInput.value : examNameDropdown.value;
    const studentYear = document.getElementById('studentYear').value;
    const studentBranch = document.getElementById('studentBranch').value;
    const studentVenue = document.getElementById('studentvenue').value;

    if (examName && studentYear && studentBranch && studentVenue) {
        // Update the exam title in the header
        document.getElementById('examTitle').innerText = 
            `Exam Name: ${examName} | Year: ${studentYear} | Branch: ${studentBranch} | Venue: ${studentVenue}`;

        // Update the exam details in the right section
        const examDetailsDisplay = document.getElementById('examDetailsDisplay');
        examDetailsDisplay.innerHTML = `
            <p><strong>Exam Name:</strong> ${examName}</p>
            <p><strong>Year:</strong> ${studentYear}</p>
            <p><strong>Branch:</strong> ${studentBranch}</p>
            <p><strong>Venue:</strong> ${studentVenue}</p>
        `;

        
        examDetailsDisplay.style.display = 'block';

        
        document.getElementById('examName').disabled = true;
        document.getElementById('customExamName').disabled = true;
        document.getElementById('studentYear').disabled = true;
        document.getElementById('studentBranch').disabled = true;
        document.getElementById('studentvenue').disabled = true;
        document.getElementById('editDetailsBtn').style.display = 'inline-block';

        mainDetailsSet = true;
    } else {
        alert('Please enter Exam Name, Student Year, Branch, and Venue.');
    }
}




// Enable Edit Mode
function enableEdit() {
    // Enable Edit Mode feature 
    document.getElementById('examName').disabled = false;
    document.getElementById('customExamName').disabled = false;
    document.getElementById('studentYear').disabled = false;
    document.getElementById('studentBranch').disabled = false;
    document.getElementById('studentvenue').disabled = false;
    document.getElementById('editDetailsBtn').style.display = 'none';
}


//---------------------------------------------------------------------------------------------------------------------------------------
//new day new motivation  , 19/2 , gulaabi akhein jo teri dekhi sharabi ye dil ho gaya 



function submitAllData() {
    if (examList.length > 0) {
        showSuccessPopup(); // Show success message
        console.log('Exam Data:', examList);
    } else {
        alert('No data to submit!');
    }
}


document.getElementById('submitButton').addEventListener('click', submitAllData);

// Fetch exam details from the backend
//need to change this part





async function loadData() {
    //helps to load pre written data from backend
    try {
        const response = await fetch('/api/exam_scheduler'); 
        const data = await response.json();
        console.log("Data from backend:", data); 

        if (data && data.exam_data && data.exam_data.length > 0) {
            const exam = data.exam_data[0]; 

            
            document.getElementById('studentYear').value = exam.studentYear || '';
            document.getElementById('studentBranch').value = exam.studentBranch || '';
            document.getElementById('studentvenue').value = exam.examVenue || '';

            if (exam.schedule && exam.schedule.length > 0) {
                examList = exam.schedule.map((item, index) => ({
                    id: index + 1,
                    subject: item.subject,
                    code: item.subjectCode, 
                    examDate: item.examDate,
                    time: item.time
                }));
                console.log("Exam List after mapping:", examList);
                renderTable();
            }

            document.getElementById('submitButton').style.display = 'inline-block';

            alert('Data loaded successfully!');
        } else {
            alert('No data found in the database.');
        }
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Failed to load data. Please try again.');
    }
}
//-----------------------------signing off -26/02/25--------------------------------- samm//