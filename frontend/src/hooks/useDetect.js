import { useMutation } from '@tanstack/react-query'
import { detectAlgas } from '../api/algae'

/**
 * Mutation hook para POST /detect/annotated
 * Usage: const { mutate, data, isPending, error } = useDetect()
 */
export function useDetect() {
  return useMutation({
    mutationFn: ({ file, conf, iou, imgsz }) =>
      detectAlgas(file, conf, iou, imgsz),
  })
}
