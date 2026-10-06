import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import CoursePage from './pages/CoursePage';
import LessonPage from './pages/LessonPage';

export default function App() {
  const [screen, setScreen]           = useState('home');
  const [course, setCourse]           = useState(null);
  const [activeLesson, setActiveLesson] = useState(null);

  const goHome       = ()         => setScreen('home');
  const showCourse   = (data)     => { setCourse(data); setScreen('course'); };
  const openLesson   = (mi, li)   => { setActiveLesson({ mi, li }); setScreen('lesson'); };
  const backToCourse = ()         => setScreen('course');

  return (
    <div className="app">
      {screen === 'home'   && <HomePage   onCourseGenerated={showCourse} />}
      {screen === 'course' && <CoursePage course={course} onOpenLesson={openLesson} onBack={goHome} />}
      {screen === 'lesson' && <LessonPage course={course} mi={activeLesson.mi} li={activeLesson.li}
                                          onBack={backToCourse} onOpenLesson={openLesson} />}
    </div>
  );
}
