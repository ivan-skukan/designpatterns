import random
from abc import ABC, abstractmethod

class GeneratorStrategy(ABC):
  @abstractmethod
  def generate(self):
    pass


class PercentileStrategy(ABC):
  @abstractmethod
  def determine_percentile(self,p,num):
    pass

class SequentialGenerator(GeneratorStrategy):
  def __init__(self,start,stop,step=1):
    if step == 0:
      raise ValueError("Step cannot be zero.")

    self.start = start
    self.stop = stop
    self.step = step

  def generate(self):
    return list(range(self.start, self.stop, self.step))



class RandomGenerator(GeneratorStrategy):
  def __init__(self, mean, std_dev, count):
    self.mean = mean
    self.std_dev = std_dev
    self.count = count

  def generate(self):
    return [int(random.gauss(self.mean, self.std_dev)) for _ in range(self.count)]

class FibonacciGenerator(GeneratorStrategy):
  def __init__(self,n):
    self.n = n
  
  def generate(self):
    return self.generate_loop(self.n)
  
  def generate_loop(self, count):
      if count <= 0:
          return []
      elif count == 1:
          return [0]
      fib = [0, 1]
      while len(fib) < count:
          fib.append(fib[-1] + fib[-2])
      return fib

class NearestRankPercentileStrategy(PercentileStrategy):
  def __init__(self):
    pass
  def determine_percentile(self, p, nums):
    nums = sorted(nums)
    N = len(nums)
    n_p = p*N/100 + 0.5
    idx = int(n_p) - 1
    if idx < 0:
      return nums[0]
    if idx >= N:
      return nums[N-1]
    return nums[idx]

class InterpolatedPercentileStrategy(PercentileStrategy):
  def __init__(self):
    pass
  def determine_percentile(self, p, nums):
    nums = sorted(nums)
    N = len(nums)
    ps = [100*(i-0.5)/N for i in range(1,N+1)]

    if p <= ps[0]:
      return nums[0]
    if p >= ps[-1]:
        return nums[-1]

    for i in range(1,N):
      if ps[i] > p:
        v_i = nums[i-1]
        v_ip1 = nums[i]

        return v_i + N * (p-ps[i-1]) * (v_ip1 - v_i) / 100

class DistributionTester:
  
  def __init__(self, generate_strategy, percentile_strategy):
    self.generate_strategy = generate_strategy
    self.percentile_strategy = percentile_strategy

  def generateNums(self):
    self.nums = self.generate_strategy.generate()

  def getPercentiles(self): 
    percentiles = range(10,100,10)

    for p in percentiles:
      print(self.percentile_strategy.determine_percentile(p, self.nums))

def run_combinations():

    test_cases = [
        # Sequential generator + Nearest Rank Percentile
        (SequentialGenerator(1, 101), NearestRankPercentileStrategy(), "Sequential + Nearest Rank"),
        
        # Sequential generator + Interpolated Percentile
        (SequentialGenerator(1, 101), InterpolatedPercentileStrategy(), "Sequential + Interpolated"),

        # Random generator + Nearest Rank Percentile
        (RandomGenerator(50, 10, 100), NearestRankPercentileStrategy(), "Random + Nearest Rank"),

        # Random generator + Interpolated Percentile
        (RandomGenerator(50, 10, 100), InterpolatedPercentileStrategy(), "Random + Interpolated"),

        # Fibonacci generator + Nearest Rank Percentile
        (FibonacciGenerator(10), NearestRankPercentileStrategy(), "Fibonacci + Nearest Rank"),

        # Fibonacci generator + Interpolated Percentile
        (FibonacciGenerator(10), InterpolatedPercentileStrategy(), "Fibonacci + Interpolated")
    ]

    for generator, percentile, description in test_cases:
        print(f"Running test: {description}")
        
        dist_tester = DistributionTester(generator, percentile)
        dist_tester.generateNums()
        
        dist_tester.getPercentiles()
        print("-" * 50)


# Run the combinations
if __name__ == "__main__":
    run_combinations()


