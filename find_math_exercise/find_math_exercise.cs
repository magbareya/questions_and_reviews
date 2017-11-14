using System;
using System.Collections.Generic;

namespace FindMathExercise
{
    class Program
    {
        static Dictionary<char, Func<long, long, long>> Operations = new Dictionary<char, Func<long, long, long>>
        {
            { '+' , (a,b) => {return a+b; } },
            { '-' , (a,b) => {return a-b; } },
            { '*' , (a,b) => {return a*b; } },
            { '/' , (a,b) => {return a/b; } }
        };

        static void Main(string[] args)
        {
            FindMathExercise(new List<long> { 1, 5, 6, 7 }, 42);
        }

        static void FindMathExercise(List<long> nums, long result)
        {
            var stack = new Stack<object>();
            foreach (var n in nums)
            {
                stack.Push(n);
                var new_list = new List<long>(nums);
                new_list.Remove(n);
                FindMathExerciseInternal(new_list, stack, 0, result);
                stack.Pop();
            }
        }

        static void FindMathExerciseInternal(List<long> available_nums, Stack<object> stack, int opsNum, long result)
        {
            if (opsNum > 0)
            {
                foreach (var op in Operations.Keys)
                {
                    stack.Push(op);
                    FindMathExerciseInternal(available_nums, stack, opsNum - 1, result);
                    stack.Pop();
                }
            }

            if (available_nums.Count == 0)
            {
                if (opsNum == 0)
                {
                    var ex = StackToMathExercise(Clone(stack));
                    var value = EvaluateStack(Clone(stack));
                    if (value.HasValue && Abs(value.Value, result) < 0.001)
                        Console.WriteLine(ex);
                    return;
                }
            }
            else
            {
                foreach (var n in available_nums)
                {
                    stack.Push(n);
                    var new_list = new List<long>(available_nums);
                    new_list.Remove(n);
                    FindMathExerciseInternal(new_list, stack, opsNum + 1, result);
                    stack.Pop();
                }
            }
        }

        static string StackToMathExercise(Stack<object> stack)
        {
            if (stack.Count == 0)
                throw new Exception("Error size 0");
            var top = stack.Pop();
            if (top is int || top is long)
                return top.ToString();
            else if (top is char)
            {
                var left = StackToMathExercise(stack);
                var right = StackToMathExercise(stack);
                return String.Format("( {0} {1} {2} )", left, top, right);
            }
            else
                throw new Exception("Unknown element");
        }

        static long? EvaluateStack(Stack<object> stack)
        {
            if (stack.Count == 0)
                throw new Exception("Error size 0");
            var top = stack.Pop();
            if (top is int || top is long)
                return (long)Convert.ChangeType(top, typeof(long));
            else if (top is char)
            {
                var left = EvaluateStack(stack);
                var right = EvaluateStack(stack);
                var operation = Operations[(char)top];
                if (left == null || right == null || ((char)top == '/' && right == 0))
                    return null;
                return operation(left.Value, right.Value);
            }
            else
                throw new Exception("Unknown element");
        }

        public static Stack<T> Clone<T>(Stack<T> stack)
        {
            return new Stack<T>(new Stack<T>(stack));
        }

        public static Stack<T> Reverse<T>(Stack<T> stack)
        {
            return new Stack<T>(stack);
        }


        static long Abs(long a, long b)
        {
            return (a >= b) ? a - b : b - a;
        }
    }
}