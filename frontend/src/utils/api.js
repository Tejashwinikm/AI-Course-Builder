import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

export const generateCourse   = (topic, level, numModules) =>
  api.post('/course/generate', { topic, level, num_modules: numModules });

export const generateQuiz     = (topic, moduleTitle, lessonTitle, keyConcepts) =>
  api.post('/quiz/generate', { topic, module_title: moduleTitle, lesson_title: lessonTitle, key_concepts: keyConcepts });

export const searchVideos     = (q, n = 3) =>
  api.get('/video/search', { params: { q, n } });

export const generateNotes    = (topic, lessonTitle, videoId, keyConcepts) =>
  api.post('/notes/generate', { topic, lesson_title: lessonTitle, video_id: videoId, key_concepts: keyConcepts });

export const registerCourse   = (courseId, courseTitle, topic, totalLessons, totalQuizzes) =>
  api.post('/progress/register', { course_id: courseId, course_title: courseTitle, topic, total_lessons: totalLessons, total_quizzes: totalQuizzes });

export const completeLesson   = (courseId, moduleIndex, lessonIndex, lessonType, quizScore = null, quizTotal = null) =>
  api.post('/progress/complete', { course_id: courseId, module_index: moduleIndex, lesson_index: lessonIndex, lesson_type: lessonType, quiz_score: quizScore, quiz_total: quizTotal });

export const getProgress      = (courseId) =>
  api.get(`/progress/${courseId}`);

export const askMentor        = (topic, lessonTitle, lessonSummary, keyConcepts, progressPct, conversationHistory, question) =>
  api.post('/mentor/ask', { topic, lesson_title: lessonTitle, lesson_summary: lessonSummary, key_concepts: keyConcepts, progress_pct: progressPct, conversation_history: conversationHistory, question });

export const checkHealth      = () => api.get('/health');
