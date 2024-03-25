import { getRandomNumber } from 'pages/static/pages/random_number/random_number'

describe('getRandomNumber', () => {
  afterEach(() => {
    jest.spyOn(global.Math, 'random').mockRestore();
  })

  it('should return ceil 100x Math.random()', () => {
    jest.spyOn(global.Math, 'random').mockReturnValue(0.123456789)
    const randomNumber = getRandomNumber()
    expect(randomNumber).toBe(13)
  })

  it('should return a number between 1 and 100', () => {
    jest.spyOn(global.Math, 'random').mockReturnValue(0)
    const lowerBound = getRandomNumber()
    expect(lowerBound).toEqual(1)
    jest.spyOn(global.Math, 'random').mockReturnValue(0.9999999999999999)
    const higherBound = getRandomNumber()
    expect(higherBound).toEqual(100)
  })
})
