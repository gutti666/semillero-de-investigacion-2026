import { useMutation } from '@tanstack/react-query'
import { classifyAlga } from '../api/algae'

/**
 * Mutation hook para POST /detect
 * Usage: const { mutate, data, isPending, error } = useClassify()
 */
export function useClassify() {
  return useMutation({
    mutationFn: ({ file, conf, iou, imgsz }) =>
      classifyAlga(file, conf, iou, imgsz),
  })
}
