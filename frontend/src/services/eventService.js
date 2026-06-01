import api from './api';

export const eventService = {
  list(params) {
    return api.get('/events/', { params });
  },

  create(data) {
    return api.post('/events/', data);
  },

  retrieve(id) {
    return api.get(`/events/${id}/`);
  },

  update(id, data) {
    return api.put(`/events/${id}/`, data);
  },

  partialUpdate(id, data) {
    return api.patch(`/events/${id}/`, data);
  },

  destroy(id) {
    return api.delete(`/events/${id}/`);
  },

  changeStatus(id, status) {
    return api.patch(`/events/${id}/status/`, { status });
  },
};
