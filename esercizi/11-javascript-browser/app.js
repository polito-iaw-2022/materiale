'use strict';

function Exam(code, name, credits, date, score) {
  this.code = code;
  this.name = name;
  this.credits = credits;
  this.date = dayjs(date);
  this.score = score;
}

function ExamList() {
  this.list = [];

  this.init = () => {
    this.list.push(
      new Exam('16ACF', 'Analisi matematica I', 10, '2021-02-01', 28),
      new Exam('15AHM', 'Chimica', 8, '2021-02-15', 21),
      new Exam('14BHD', 'Informatica', 8, '2021-02-06', 30),
    );
  };

  this.getAll = () => {
    return this.list;
  }
}

function createTableRow2(exam) {
  return `<tr>
    <td>${exam.date.format('YYYY-MM-DD')}</td>
    <td>${exam.name}</td>
    <td>${exam.credits}</td>
    <td>${exam.score}</td>
    <td><button id="${exam.code}" class="btn btn-danger">X</button></td>
  </tr>`;
}

function createTableRow(exam) {
  const tr = document.createElement('tr');

  const tdDate = document.createElement('td');
  tdDate.innerText = exam.date.format('YYYY-MM-DD');
  tr.appendChild(tdDate);

  const tdName = document.createElement('td');
  tdName.innerText = exam.name;
  tr.appendChild(tdName);

  const tdCredits = document.createElement('td');
  tdCredits.innerText = exam.credits;
  tr.appendChild(tdCredits);

  const tdScore = document.createElement('td');
  tdScore.innerText = exam.score;
  tr.appendChild(tdScore);

  const tdAction = document.createElement('td');
  const button = document.createElement('button');
  button.id = exam.code;
  button.className = 'btn btn-danger';
  button.innerText = 'X';
  tdAction.append(button);
  tr.appendChild(tdAction);

  tdAction.addEventListener('click', e => {
    tr.remove();
    //console.log(e.target.id);
  })

  return tr;
}

function fillExamTable(exams) {
  const examTable = document.querySelector('#exam-table');
  // const examTable = document.getElementById('exam-table');
  for (const exam of exams) {
    const examEl = createTableRow(exam);
    // classic way:
    examTable.prepend(examEl);
    // string literal way:
    //examTable.insertAdjacentHTML('afterbegin', examEl);
  }
}

/* Main */
const examList = new ExamList();
examList.init();
const exams = examList.getAll();
fillExamTable(exams);