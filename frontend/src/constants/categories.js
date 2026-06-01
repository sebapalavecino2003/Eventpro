export const EVENT_CATEGORIES = [
  { value: 'conference', label: 'Conferencia' },
  { value: 'workshop', label: 'Taller' },
  { value: 'seminar', label: 'Seminario' },
  { value: 'networking', label: 'Networking' },
  { value: 'social', label: 'Social' },
  { value: 'corporate', label: 'Corporativo' },
  { value: 'other', label: 'Otro' },

];

export const CATEGORY_LABELS = Object.fromEntries(
  EVENT_CATEGORIES.map((c) => [c.value, c.label])
);

export const CATEGORY_VALUES = EVENT_CATEGORIES.map((c) => c.value);

export function getCategoryLabel(value) {
  return CATEGORY_LABELS[value] || value;
}
