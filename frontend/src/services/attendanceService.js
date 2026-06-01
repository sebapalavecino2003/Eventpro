import api from './api';

export const attendanceService = {
  checkIn(data) {
    return api.post('/attendance/checkin/', data);
  },

  history(params) {
    return api.get('/attendance/', { params });
  },
};
