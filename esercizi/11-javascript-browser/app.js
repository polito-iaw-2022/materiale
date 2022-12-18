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

function fillExamTable(exams) {
  /* Write something clever */
}

/* Main */
const examList = new ExamList();
examList.init();
const exams = examList.getAll();
fillExamTable(exams);