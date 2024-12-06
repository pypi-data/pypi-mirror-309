use std::ops::Not;

use super::digits::InvertComponents;
use super::types::BigInt;

impl<Digit: InvertComponents, const DIGIT_BITNESS: usize> Not
    for &BigInt<Digit, DIGIT_BITNESS>
{
    type Output = BigInt<Digit, DIGIT_BITNESS>;

    fn not(self) -> Self::Output {
        let (sign, digits) =
            Digit::invert_components::<DIGIT_BITNESS>(self.sign, &self.digits);
        Self::Output { sign, digits }
    }
}

impl<Digit: InvertComponents, const DIGIT_BITNESS: usize> Not
    for BigInt<Digit, DIGIT_BITNESS>
{
    type Output = Self;

    fn not(self) -> Self::Output {
        let (sign, digits) =
            Digit::invert_components::<DIGIT_BITNESS>(self.sign, &self.digits);
        Self { sign, digits }
    }
}
